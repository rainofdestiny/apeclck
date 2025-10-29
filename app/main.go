package main

import (
	"log"
	"net/http"

	"app/api"
	"app/shortener"
	"app/storage"
)

func main() {
	store := storage.NewRedisStorage("redis:6379", "")
	service := shortener.NewService(store)
	handler := api.NewHandler(service)

	mux := http.NewServeMux()
	mux.HandleFunc("/shorten", handler.Shorten)
	mux.HandleFunc("/", handler.Resolve)

	log.Println("Server running on :8080")
	log.Fatal(http.ListenAndServe(":8080", mux))
}
