"""
FastAPI 服务启动/重启/停止工具。

用法:
    python run_server.py            启动服务（若端口已被占用则提示）
    python run_server.py restart    重启服务（先杀掉占用端口的旧进程，再启动）
    python run_server.py stop       停止服务（杀掉占用端口的进程）

可选参数:
    --port 8000   指定端口，覆盖默认值 8000

注意:
    服务以单进程模式运行（不带 --reload），避免 milvus-lite 本地数据库
    （data/oncall_agent.db）因多进程争抢独占锁导致 ConnectionConfigException。
"""

import argparse
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent

# 用当前正在运行本脚本的解释器（fastapi 环境）启动 uvicorn，
# 保证启动服务与运行脚本共用同一个 python 环境。
PYTHON = Path(sys.executable).resolve()

DEFAULT_PORT = 8000
MYSQL_CONTAINER = "oncall-agent-mysql"


def get_listener_pids(port: int) -> list:
    """返回本地端口上处于 LISTENING 状态的进程 PID 列表。"""
    try:
        result = subprocess.run(
            ["netstat", "-ano"], capture_output=True, text=True
        )
    except FileNotFoundError:
        return []
    pids = []
    for line in result.stdout.splitlines():
        tokens = line.split()
        if len(tokens) < 5:
            continue
        local_addr, state, pid = tokens[1], tokens[3], tokens[4]
        if state == "LISTENING" and local_addr.endswith(":" + str(port)):
            if pid.isdigit() and pid not in pids:
                pids.append(pid)
    return pids


def kill_processes(pids: list) -> None:
    """终止指定 PID 的进程；在 Windows 上使用 taskkill 连同子进程一起结束。"""
    for pid in pids:
        if os.name == "nt":
            subprocess.run(["taskkill", "/PID", pid, "/F", "/T"],
                           capture_output=True)
        else:
            try:
                os.kill(int(pid), signal.SIGKILL)
            except ProcessLookupError:
                pass
        print(f"[stop] 已结束进程 {pid}")


def mysql_ready() -> bool:
    """检查 MySQL 容器是否已经就绪（已启动且可 ping）。"""
    try:
        result = subprocess.run(
            ["docker", "exec", MYSQL_CONTAINER, "mysqladmin", "ping",
             "-uoncall", "-poncall", "--silent"],
            capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return True


def start_mysql() -> None:
    """启动 MySQL 容器并等待就绪（借鉴 start-dev.ps1 逻辑，最长 60s）。"""
    print("[1/2] 检查 MySQL 容器...")
    if mysql_ready():
        print("[1/2] MySQL 已就绪")
        return
    print("[1/2] 启动 MySQL 容器（docker compose up -d）...")
    try:
        subprocess.run(["docker", "compose", "up", "-d"],
                       cwd=PROJECT_DIR, check=True, capture_output=True)
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        print(f"[1/2] 启动 MySQL 失败：{exc}")
        return

    for _ in range(30):
        if mysql_ready():
            print("[1/2] MySQL 已就绪")
            return
        time.sleep(2)
    print("[1/2] 警告：等待 MySQL 超时（60s），继续启动服务...")


def start_server(port: int) -> None:
    """以单进程模式启动 uvicorn，前台运行（Ctrl+C 停止）。"""
    pids = get_listener_pids(port)
    if pids:
        print(f"[start] 端口 {port} 已被进程占用：{', '.join(pids)}")
        print("[start] 如需重启请使用: python run_server.py restart")
        return

    if not PYTHON.exists():
        print(f"[start] 未找到 python：{PYTHON}")
        sys.exit(1)

    print(f"[start] 启动 FastAPI 于 http://127.0.0.1:{port}")
    cmd = [
        str(PYTHON), "-m", "uvicorn", "main:app",
        "--host", "127.0.0.1", "--port", str(port),
    ]
    # 前台阻塞运行；Ctrl+C 停止后，进程随之结束
    try:
        proc = subprocess.run(cmd, cwd=PROJECT_DIR)
        sys.exit(proc.returncode)
    except KeyboardInterrupt:
        print("[start] 服务已停止")
        sys.exit(0)


def stop_server(port: int) -> None:
    pids = get_listener_pids(port)
    if not pids:
        print(f"[stop] 端口 {port} 上没有正在运行的服务")
        return
    kill_processes(pids)
    print(f"[stop] 端口 {port} 的服务已停止")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="FastAPI 服务启动/重启/停止工具")
    parser.add_argument("action", nargs="?", default="start",
                        choices=["start", "restart", "stop"])
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    args = parser.parse_args()

    start_mysql()

    if args.action == "stop":
        stop_server(args.port)
        return

    if args.action == "restart":
        stop_server(args.port)
        time.sleep(1)

    start_server(args.port)


if __name__ == "__main__":
    main()