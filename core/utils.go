package core

import (
	"strconv"

	"github.com/google/uuid"
)

func GetUUID() string {
	u2, _ := uuid.NewUUID()
	return u2.String()
}

func Float64(str string) float64 {
	f, _ := strconv.ParseFloat(str, 64)
	return f
}
