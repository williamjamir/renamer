def test_env():
    import os
    print("Going to print all envs:")
    for name in ('LOGNAME', 'USER', 'LNAME', 'USERNAME', 'TEST_FINAL'):
        user = os.environ.get(name)
        print(name, "= ", user)
        if user:
            print("True for: ", user)
