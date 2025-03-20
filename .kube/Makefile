
install-app:
	# Install APP Kubernetes cluster 
	# NameSpace + Registry + Ingress
	kubectl apply -f ns.yml
	kubectl apply -f ingress.yml
	kubectl apply -f registry.yml
	# Start Frontend 
	kubectl apply -f frontend.yml
	

clean-app:
	kubectl delete ns x5-lot14

