import encryption.kudos as kudos_encryption


def test_encrypt_decrypt():
    server_side_secret = "my-server-side-secret"
    kudo_text = "Kudos to the developers of the kudo box"
    password = kudos_encryption.make_password("kudo-box-tester", "kudos", server_side_secret)
    encrypted = kudos_encryption.encrypt(kudo_text, password)
    print(encrypted)
    decrypted = kudos_encryption.decrypt(encrypted, password)
    assert decrypted == kudo_text