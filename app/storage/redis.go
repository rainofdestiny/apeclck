package storage

import (
	"context"

	"github.com/redis/go-redis/v9"
)

type RedisStorage struct {
	client *redis.Client
}

func NewRedisStorage(addr, password string) *RedisStorage {
	rdb := redis.NewClient(&redis.Options{
		Addr:     addr,
		Password: password,
		DB:       0,
	})
	return &RedisStorage{client: rdb}
}

func (r *RedisStorage) Set(ctx context.Context, key, value string) error {
	return r.client.Set(ctx, key, value, 0).Err()
}

func (r *RedisStorage) Get(ctx context.Context, key string) (string, error) {
	return r.client.Get(ctx, key).Result()
}
