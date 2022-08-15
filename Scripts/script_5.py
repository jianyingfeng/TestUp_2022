class SoftAssertion:
    def __init__(self):
        self.success = True
        self.error_message_list = []

    def check(self, to_check, error_message):
        self.success = self.success and to_check
        if not to_check:
            self.error_message_list.append(error_message)


if __name__ == '__main__':
    soft_assert = SoftAssertion()
    a = 1
    b = 1
    c = 2
    d = 2
    soft_assert.check((a + c != 3), f"a + a should != 3, actural = {a + a}")
    soft_assert.check((a + c != 3), f"a + a should != 3, actural = {a + a}")
    assert soft_assert.success, soft_assert.error_message_list