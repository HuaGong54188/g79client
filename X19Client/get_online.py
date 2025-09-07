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
    return random.choice(lines)


def get_online_names(server_arg: str, cookies_path: str) -> list[str]:
    sauth = pick_sauth(cookies_path)
    client = G79Client(sauth)
    # 查名称，取第一个匹配
    resp = client.SearchRentalServerByName(server_arg)
    if resp.code != 0 or not resp.entities:
        return []
    server_id = str(resp.entities[0].entity_id)
    players = client.GetRentalServerPlayers(server_id, is_online=True, length=50, order_type=1)
    if players.code != 0:
        return []
    return [p.name for p in players.entities if p.is_online]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--server', required=True)
    ap.add_argument('--cookies', required=True)
    args = ap.parse_args()
    names = get_online_names(args.server, args.cookies)
    print(json.dumps(names, ensure_ascii=False))


if __name__ == '__main__':
    main()


