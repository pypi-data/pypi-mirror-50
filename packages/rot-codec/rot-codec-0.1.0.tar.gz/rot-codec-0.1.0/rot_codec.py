import os
import codecs
import click


a = ord('a')
z = ord('z')
A = ord('A')
Z = ord('Z')
i0 = ord('0')
i9 = ord('9')
ROT_MIN = 33 # !
ROT_MAX = 126 # ~

ROT5_ENCODE_RANGES = [(i0, i9, 5)]
ROT5_DECODE_RANGES = [(i0, i9, -5)]
ROT13_ENCODE_RANGES = [(A, Z, 13), (a, z, 13)]
ROT13_DECODE_RANGES = [(A, Z, -13), (a, z, -13)]
ROT18_ENCODE_RANGES = [(i0, i9, 5), (A, Z, 13), (a, z, 13)]
ROT18_DECODE_RANGES = [(i0, i9, -5), (A, Z, -13), (a, z, -13)]
ROT47_ENCODE_RANGES = [(ROT_MIN, ROT_MAX, 47)]
ROT47_DECODE_RANGES = [(ROT_MIN, ROT_MAX, -47)]

def rot(text, rot_ranges):
    result = ""
    for c in text:
        ord_c = ord(c)
        transformed = False
        for rot_range in rot_ranges:
            if rot_range[0] <= ord_c <= rot_range[1]:
                ord_c = (rot_range[1] + ord_c + rot_range[2] - 2 * rot_range[0] + 1) % (rot_range[1] - rot_range[0] + 1) + rot_range[0]
                result += chr(ord_c)
                transformed = True
                break
        if not transformed:
            result += c
    return result

def rot5_encode(text):
    return rot(text, ROT5_ENCODE_RANGES)

def rot5_decode(text):
    return rot(text, ROT5_DECODE_RANGES)

def rot13_encode(text):
    return rot(text, ROT13_ENCODE_RANGES)

def rot13_decode(text):
    return rot(text, ROT13_DECODE_RANGES)

def rot18_encode(text):
    return rot(text, ROT18_ENCODE_RANGES)

def rot18_decode(text):
    return rot(text, ROT18_DECODE_RANGES)

def rot47_encode(text):
    return rot(text, ROT47_ENCODE_RANGES)

def rot47_decode(text):
    return rot(text, ROT47_DECODE_RANGES)

def _rot5_encoder(text: str) -> str:
    result = rot5_encode(text)
    return result, len(result)

def _rot5_decoder(text: str) -> str:
    result = rot5_decode(text)
    return result, len(result)

def _rot5_search(name):
    if name == "rot5":
        return codecs.CodecInfo(_rot5_encoder, _rot5_decoder, name="rot5")
    else:
        return None

def _rot13_encoder(text: str) -> str:
    result = rot13_encode(text)
    return result, len(result)

def _rot13_decoder(text: str) -> str:
    result = rot13_decode(text)
    return result, len(result)

def _rot13_search(name):
    if name == "rot13":
        return codecs.CodecInfo(_rot5_encoder, _rot5_decoder, name="rot13")
    else:
        return None

def _rot18_encoder(text: str) -> str:
    result = rot18_encode(text)
    return result, len(result)

def _rot18_decoder(text: str) -> str:
    result = rot18_decode(text)
    return result, len(result)

def _rot18_search(name):
    if name == "rot18":
        return codecs.CodecInfo(_rot5_encoder, _rot5_decoder, name="rot18")
    else:
        return None

def _rot47_encoder(text: str) -> str:
    result = rot47_encode(text)
    return result, len(result)

def _rot47_decoder(text: str) -> str:
    result = rot47_decode(text)
    return result, len(result)

def _rot47_search(name):
    if name == "rot47":
        return codecs.CodecInfo(_rot5_encoder, _rot5_decoder, name="rot47")
    else:
        return None

codecs.register(_rot5_search)
codecs.register(_rot13_search)
codecs.register(_rot18_search)
codecs.register(_rot47_search)

def get_content(content, encoding="utf-8"):
    if not content:
        if hasattr(os.sys.stdin, "reconfigure"):
            os.sys.stdin.reconfigure(encoding=encoding)
            content = os.sys.stdin.read()
            return content
        else:
            import codecs
            content = codecs.getreader(encoding)(os.sys.stdin).read()
            return content
    if os.path.exists(content):
        with open(content, "r", encoding=encoding) as fobj:
            return fobj.read()
    return content

@click.command()
@click.option("-m", "--method", type=click.Choice(["rot5", "rot13", "rot18", "rot47"]), default="rot13")
@click.option("-d", "--decode", is_flag=True)
@click.option("-e", "--encoding", default="utf-8", help="Message encoding.")
@click.argument("message", nargs=1, required=False)
def rot_cli(method, decode, encoding, message):
    """ROT5、ROT13、ROT18、ROT47 编码是一种简单的码元位置顺序替换暗码。此类编码具有可逆性，可以自我解密，主要用于应对快速浏览，或者是机器的读取，而不让其理解其意。

ROT5 是 rotate by 5 places 的简写，意思是旋转5个位置，其它皆同。下面分别说说它们的编码方式。

ROT5：只对数字进行编码，用当前数字往前数的第5个数字替换当前数字，例如当前为0，编码后变成5，当前为1，编码后变成6，以此类推顺序循环。

ROT13：只对字母进行编码，用当前字母往前数的第13个字母替换当前字母，例如当前为A，编码后变成N，当前为B，编码后变成O，以此类推顺序循环。

ROT18：这是一个异类，本来没有，它是将ROT5和ROT13组合在一起，为了好称呼，将其命名为ROT18。

ROT47：对数字、字母、常用符号进行编码，按照它们的ASCII值进行位置替换，用当前字符ASCII值往前数的第47位对应字符替换当前字符，例如当前为小写字母z，编码后变成大写字母K，当前为数字0，编码后变成符号_。用于ROT47编码的字符其ASCII值范围是33－126，具体可参考ASCII编码。

备注：MESSAGE为提供时，则从STDIN中读取。
    """
    message = get_content(message, encoding)
    if not decode:
        result = codecs.encode(message, method)
    else:
        result = codecs.decode(message, method)
    click.echo(result)

if __name__ == "__main__":
    rot_cli()
