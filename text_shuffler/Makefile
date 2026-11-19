build_go:
	@echo "Building Go project..."
	@go build -o text_shuffler
	@echo "Build completed successfully."

build_go_win:
	@echo "Building Go project for Windows..."
	@GOOS=windows GOARCH=amd64 go build -o text_shuffler.exe
	@echo "Build completed successfully for Windows."

build_rust:
	@echo "Building Rust project..."
	@cargo build --release
	@echo "Build completed successfully."

build_rust_win:
	@echo "Building Rust project for Windows..."
	@cargo build --release --target x86_64-pc-windows-gnu
	@echo "Build completed successfully for Windows."
