#!/bin/bash
# Hermes Caller — full product install, no dependencies, no keys.
set -e
python3 --version
[ -f .env ] || cp .env.example .env
echo ".env created from .env.example — fill your OWN keys there, never commit it."
python3 tests/test_wholesale.py | tail -1
python3 tests/test_personas.py | tail -1
python3 tests/test_production.py | tail -1
python3 tests/test_inbound.py | tail -1
python3 tests/test_warrior.py | tail -1
python3 tests/test_real_dialer.py | tail -1
python3 tests/test_product.py | tail -1
python3 -m unittest discover -s tests 2>&1 | tail -2
rm -rf .framework
python3 run.py doctor
echo "INSTALLED. Next: python3 run.py dashboard  (opens http://127.0.0.1:8768)"
echo "Live call still needs: Twilio/Vapi account + keys in .env + approved packet + your test number first."
