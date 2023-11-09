SCRIPTS := process.py scrape.py

.PHONY:

clean:
	find data/databases/ data/processed/ data/unprocessed/ data/characterization -type f ! \( -name '*.md' -o -name '.gitignore' \) -exec rm -f {} \;

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