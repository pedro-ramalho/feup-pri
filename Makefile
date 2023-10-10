SCRIPTS := extract.py observations.py occurrences.py species.py

.PHONY:

clean:
	rm -rf data/databases/* data/processed/* data/unprocessed/*

run: clean
	for script in $(SCRIPTS); do \
		python3 scripts/$$script; \
	done

run_single:
	@read -p "Enter the name of the script you want to run: " script; \
	if [ -f scripts/$$script ]; then \
		python3 scripts/$$script; \
	else \
		echo "Script '$$script' not found."; \
	fi