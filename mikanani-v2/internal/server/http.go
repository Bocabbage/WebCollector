package server

import (
	"crypto/tls"
	v2 "mikanani-v2/api/mikanani/v2"
	"mikanani-v2/internal/conf"
	"mikanani-v2/internal/service"

	"github.com/go-kratos/kratos/v2/log"
	"github.com/go-kratos/kratos/v2/middleware/recovery"
	"github.com/go-kratos/kratos/v2/transport/http"
)

// NewHTTPServer new an HTTP server.
func NewHTTPServer(c *conf.Server, mikanani *service.MikananiServiceService, logger log.Logger) *http.Server {
	var opts = []http.ServerOption{
		http.Middleware(
			recovery.Recovery(),
		),
	}
	if c.Http.Network != "" {
		opts = append(opts, http.Network(c.Http.Network))
	}
	if c.Http.Addr != "" {
		opts = append(opts, http.Address(c.Http.Addr))
	}
	if c.Http.Timeout != nil {
		opts = append(opts, http.Timeout(c.Http.Timeout.AsDuration()))
	}
	if c.Tls.Cert != "" && c.Tls.Key != "" {
		cert, err := tls.LoadX509KeyPair(c.Tls.Cert, c.Tls.Key)
		if err != nil {
			log.NewHelper(logger).Warnf("Tls init failed: %v", err)
		} else {
			opts = append(opts, http.TLSConfig(&tls.Config{Certificates: []tls.Certificate{cert}}))
		}
	}
	srv := http.NewServer(opts...)
	v2.RegisterMikananiServiceHTTPServer(srv, mikanani)
	return srv
}
