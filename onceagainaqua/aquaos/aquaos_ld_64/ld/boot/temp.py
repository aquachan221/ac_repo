with open(r"D:\aqua\code\aqua.os\aquaos_ld_64\ld\boot\core_extracted.img", "rb") as f:
    magic = f.read(4)
    print("Magic Bytes:", magic.hex())