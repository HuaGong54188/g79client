#!/usr/bin/env python3
import argparse
import json
import os
import random
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'X19Client'))
from X19Client import X19Client as G79Client  # type: ignore


def pick_sauth(cookies_path: str) -> str:
    with open(cookies_path, 'r', encoding='utf-8') as f:
        lines = [ln.strip() for ln in f.readlines() if ln.strip()]
    if not lines:
        raise RuntimeError('no cookies')
    # 随机挑选一条，保持与 Go 侧一致
    return random.choice(lines)


def get_capacity(server_arg: str, cookies_path: str) -> int:
    sauth = pick_sauth(cookies_path)
    client = G79Client(sauth)
    # 通过名称搜索，取第一个匹配项
    resp = client.SearchRentalServerByName(server_arg)
    if resp.code != 0 or not resp.entities:
        raise RuntimeError('search server failed')
    server_id = str(resp.entities[0].entity_id)
    details = client.GetRentalServerDetails(server_id)
    if details.code != 0:
        raise RuntimeError('get details failed')
    return int(details.entity.capacity)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--server', required=True)
    ap.add_argument('--cookies', required=True)
    args = ap.parse_args()
    cap = get_capacity(args.server, args.cookies)
    print(str(cap))


if __name__ == '__main__':
    main()


