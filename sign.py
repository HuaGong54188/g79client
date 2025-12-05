import struct
import base64


shift_table = [0x0D0A0601, 0x0E090502, 0x30B0704, 0x50B0803, 0xE0B0701]
const_table = [
    0xF61E2562, 0xC040B340, 0x265E5A51, 0xE9B6C7AA,
    0xA4BEEA44, 0x4BDECFA9, 0xF6BB4B60, 0xBEBFBC70,
    0x655B59C3, 0x8F0CCC92, 0xFFEFF47D, 0x85845DD1,
    0x289B7EC6, 0xEAA127FA, 0xD4EF3085, 0x04881D05,
    0x21E1CDE6, 0xC33707D6, 0xF4D50D87, 0x455A14ED,
    0xF61E2562, 0xC040B340, 0x265E5A51, 0xE9B6C7AA,
    0xA4BEEA44, 0x4BDECFA9, 0xF6BB4B60, 0xBEBFBC70,
    0x655B59C3, 0x8F0CCC92, 0xFFEFF47D, 0x85845DD1,
    0x289B7EC6, 0xEAA127FA, 0xD4EF3085, 0x04881D05,
    0x21E1CDE6, 0xC33707D6, 0xF4D50D87, 0x455A14ED,
]

def encrypt(message: bytes, offset: int, rounds: int):
    """
    :param message: 网易的message字符串
    :param offset: 增量
    :param rounds: 偏移
    :return: base64编码
    """

    # 判断message是不是空的
    if not message:
        return ""

    data = message
    # 用字符串0填充message到是4的倍数
    while len(data) % 4 != 0:
        data += '0'

    group = []
    for i in range(0, len(data), 4):
        b = data[i:i + 4]
        group.append(struct.unpack('>I', b.encode())[0])

    while (len(group) % 64 != 0):
        group.append(0xABCDE987)

    # 拆出4个1字节的 uint32_t
    shiftBase = shift_table[offset]
    bytes_data = struct.pack('<I', shiftBase)  # < 表示小端，I 表示4字节无符号整数
    s0, s1, s2, s3 = struct.unpack('BBBB', bytes_data)  # 4B 表示4个无符号字节

    # 常数表
    # 每个 offset 对应 constTable 中连续 4 个常数。
    cb = offset * 4
    c0 = const_table[cb]
    c1 = const_table[cb + 1]
    c2 = const_table[cb + 2]
    c3 = const_table[cb + 3]

    # 初始向量（IV）
    # 四个就是 MD5 标准初始值
    hA = 0x67452301
    hB = 0xEFCDAB89
    hC = 0x98BADCFE
    hD = 0x10325476

    # 6. 轮函数
    for _ in range(rounds):
        for i in range(0, len(group), 4):
            chunk = group[i]

            # 注意每一步都 & 0xFFFFFFFF 保证 32bit 行为
            t = (chunk + c0 + ((hB & hC) | (hD & ~hB)) + hA) & 0xFFFFFFFF
            hA = (hB + ((t << s0) & 0xFFFFFFFF)) & 0xFFFFFFFF
            t = (hA + chunk + c1 + (((hC & ~hD) | (hD & hB)))) & 0xFFFFFFFF
            hB = (hB + ((t << s1) & 0xFFFFFFFF)) & 0xFFFFFFFF
            t = (hA + chunk + c2 + (hB ^ hD ^ hC)) & 0xFFFFFFFF
            hC = (hB + ((t << s2) & 0xFFFFFFFF)) & 0xFFFFFFFF
            t = (hA + chunk + c3 + (hC ^ (hB | hD))) & 0xFFFFFFFF
            hD = (hB + ((t << s3) & 0xFFFFFFFF)) & 0xFFFFFFFF

    # 7. 小端序输出 16 字节
    out = bytearray(16)
    for i in range(4):
        out[i] = (hA >> (8 * i)) & 0xFF
        out[i + 4] = (hB >> (8 * i)) & 0xFF
        out[i + 8] = (hC >> (8 * i)) & 0xFF
        out[i + 12] = (hD >> (8 * i)) & 0xFF

    return base64.b64encode(bytes(out)).decode()

if __name__ == '__main__':

    print(encrypt("3.6.5.281774815873bdd82cb7a4ce422da361f7d60d3.6.18.28312722c622f4245a37ec3f1012a5325ddc252b3e7ca013bb30a74d822579860c042b8888777a-03ff-4075-a3f3-e30363cc763b", 2, 9))