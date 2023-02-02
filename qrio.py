#%%
import base64
import pyqrcode
from pathlib import Path
from PIL import Image
from pyzbar.pyzbar import decode


def decode_qr(qr_dir, outfp=None):
    all_s = ''
    for img in sorted(Path(qr_dir).glob("*.png")):
        s = decode_img(img)
        all_s += s
    if outfp is not None:
        with open(outfp, "w", encoding="utf-8") as f:
            f.write(all_s)
    else:
        return all_s

def decode_img(img):
    img = Image.open(img)
    decocdeQR = decode(img)[0]
    s = decocdeQR.data #.decode('ascii')
    return decode_base64(s)


def encode_txt(fp, outdir=None):
    with open(fp, encoding="utf-8") as f:
        ascii_encoded_bytes = encode_base64(f.read())
    
    # Create output dir
    if outdir is None:
        outdir = Path(f"QR_{Path(fp).stem}")
    else:
        outdir = Path(outdir)
    outdir.mkdir(exist_ok=True)

    # Encode chunk of codes to QR code
    outfp = []
    d = chunk(ascii_encoded_bytes, size=1200)
    for i, p in enumerate(d):
        qr = pyqrcode.create(p)
        img = outdir / f'qr_{i}.png'
        qr.png(img, scale=5)
        outfp.append(img)
    return outfp


def chunk(string, size):
    chunks = [string[i:i+size] for i in range(0, len(string), size)]
    return chunks

def encode_base64(s):
    s_bytes = s.encode('utf-8')
    return base64.b64encode(s_bytes)

def decode_base64(bytes):
    bytes = base64.b64decode(bytes)
    s = bytes.decode('utf-8')
    return s


if __name__ == '__main__':
    encode_txt("script.R")
    decode_qr("QR_script", outfp="script-decoded.R")
