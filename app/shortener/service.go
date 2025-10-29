package shortener

import (
	"context"
	"crypto/rand"
	"encoding/base64"
)

type Storage interface {
	Set(ctx context.Context, key, value string) error
	Get(ctx context.Context, key string) (string, error)
}

type Service struct {
	storage Storage
}

func NewService(s Storage) *Service {
	return &Service{storage: s}
}

func (s *Service) Shorten(ctx context.Context, url string) (string, error) {
	b := make([]byte, 6)
	_, _ = rand.Read(b)
	key := base64.URLEncoding.EncodeToString(b)
	err := s.storage.Set(ctx, key, url)
	return key, err
}

func (s *Service) Resolve(ctx context.Context, key string) (string, error) {
	return s.storage.Get(ctx, key)
}
