import encryption.kudos as kudos_encryption


def test_encrypt_decrypt():
    server_side_secret = "hPCFZ3nrCfCHh_GIkqHtTpNCt2lyLj2u16npQLeZ9PQ="
    kudo_text = "Kudos to the developers of the kudo box"
    encrypted = kudos_encryption.encrypt(kudo_text, server_side_secret)
    print(encrypted)
    decrypted = kudos_encryption.decrypt(encrypted, server_side_secret)
    assert decrypted == kudo_text
