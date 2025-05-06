.PHONY: images

all: images

images:	
	docker build -t cpu_max -f images/cpu/Dockerfile.cpu_max images/cpu 
	docker build -t periodic_cpu_spikes -f images/cpu/Dockerfile.periodic_cpu_spikes images/cpu
	docker build -t random_cpu -f images/cpu/Dockerfile.random_cpu images/cpu
	docker build -t bursty_io -f images/io/Dockerfile.bursty_io images/io
	docker build -t continuous_io -f images/io/Dockerfile.continuous_io images/io
	docker build -t random_io -f images/io/Dockerfile.random_io images/io
	docker build -t gradual_mem_leak -f images/memory/Dockerfile.gradual_mem_leak images/memory
	docker build -t high_mem -f images/memory/Dockerfile.high_mem images/memory
	docker build -t random_mem -f images/memory/Dockerfile.random_mem images/memory
	docker build -t bursty_network -f images/network/Dockerfile.bursty_network images/network
	docker build -t high_bw -f images/network/Dockerfile.high_bw images/network
	docker build -t packet_loss -f images/network/Dockerfile.packet_loss images/network