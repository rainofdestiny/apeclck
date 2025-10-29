package api

import (
	"context"
	"encoding/json"
	"net/http"
	"strings"

	"app/shortener"
)

type Handler struct {
	service *shortener.Service
}

func NewHandler(s *shortener.Service) *Handler {
	return &Handler{service: s}
}

func (h *Handler) Shorten(w http.ResponseWriter, r *http.Request) {
	type req struct {
		URL string `json:"url"`
	}

	var body req
	if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
		http.Error(w, "invalid body", http.StatusBadRequest)
		return
	}

	key, err := h.service.Shorten(context.Background(), body.URL)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	json.NewEncoder(w).Encode(map[string]string{"short_url": "/" + key})
}

func (h *Handler) Resolve(w http.ResponseWriter, r *http.Request) {
	key := strings.TrimPrefix(r.URL.Path, "/")
	if key == "" {
		http.Error(w, "missing key", http.StatusBadRequest)
		return
	}

	url, err := h.service.Resolve(context.Background(), key)
	if err != nil {
		http.Error(w, "not found", http.StatusNotFound)
		return
	}

	http.Redirect(w, r, url, http.StatusFound)
}
