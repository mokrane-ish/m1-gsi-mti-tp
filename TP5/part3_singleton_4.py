import sqlite3


class LimitedDatabasePool:
    _instances = []
    _max_instances = 3
    _next_index = 0

    def __new__(cls, db_name=":memory:"):
        if len(cls._instances) < cls._max_instances:
            instance = super().__new__(cls)
            instance.pool_id = len(cls._instances) + 1
            instance.connection = sqlite3.connect(db_name)
            cls._instances.append(instance)
            print(f"Created new DB connection instance #{instance.pool_id}")
            return instance
        else:
            # Reuse existing instances in round-robin order once the limit is reached
            instance = cls._instances[cls._next_index]
            cls._next_index = (cls._next_index + 1) % cls._max_instances
            print(f"Max limit ({cls._max_instances}) reached -> Reusing instance #{instance.pool_id}")
            return instance

    @classmethod
    def close_all(cls):
        for inst in cls._instances:
            if inst.connection:
                inst.connection.close()
        cls._instances.clear()
        cls._next_index = 0
        print("All pooled connections closed.")


if __name__ == "__main__":
    # Request 5 connections with a maximum pool size of 3
    c1 = LimitedDatabasePool()
    c2 = LimitedDatabasePool()
    c3 = LimitedDatabasePool()
    c4 = LimitedDatabasePool()
    c5 = LimitedDatabasePool()

    print("\nTotal active instances in pool:", len(LimitedDatabasePool._instances))
    assert c4 is c1
    assert c5 is c2
    print("Assertion passed: c4 reuses c1, and c5 reuses c2.")

    LimitedDatabasePool.close_all()