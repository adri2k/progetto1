from datetime import datetime, timedelta, timezone
from math import exp



WORLD_POPULATION = 12_200_000_000

# Distribuzione molto semplificata della popolazione sui fusi orari.
TIMEZONE_WEIGHTS = {
	-5: 0.04,
	-4: 0.03,
	-3: 0.04,
	-1: 0.01,
	0: 0.02,
	1: 0.06,
	2: 0.07,
	3: 0.09,
	4: 0.05,
	5: 0.17,
	6: 0.11,
	7: 0.08,
	8: 0.11,
	9: 0.07,
	10: 0.03,
	11: 0.01,
	12: 0.01,
	13: 0.01,
}

# La funzione gaussiana per modellare i picchi di consumo durante i pasti.
def gaussian_peak(hour, center, width):
	return exp(-((hour - center) ** 2) / (2 * width ** 2))

# La probabilità di mangiare in un dato momento, basata sui picchi di colazione, pranzo e cena.
def eating_probability(local_hour):
	breakfast = 0.06 * gaussian_peak(local_hour, 8.0, 1.0)
	lunch = 0.12 * gaussian_peak(local_hour, 13.0, 1.2)
	dinner = 0.15 * gaussian_peak(local_hour, 20.0, 1.5)
	snack = 0.01
	return min(breakfast + lunch + dinner + snack, 0.35)


# La probabilità di dormire è più alta nelle ore notturne e minima durante il giorno.
def sleeping_probability(local_hour):
	night_sleep = 0.72 * gaussian_peak(local_hour, 2.0, 2.6)
	late_sleep = 0.45 * gaussian_peak(local_hour, 23.0, 1.8)
	early_morning = 0.28 * gaussian_peak(local_hour, 5.0, 1.8)
	return min(night_sleep + late_sleep + early_morning, 0.92)


def estimated_people_eating_now(current_utc=None):
	if current_utc is None:
		current_utc = datetime.now(timezone.utc)

	estimated_people = 0

	for utc_offset, weight in TIMEZONE_WEIGHTS.items():
		local_time = current_utc + timedelta(hours=utc_offset)
		local_hour = local_time.hour + (local_time.minute / 60)
		people_in_timezone = WORLD_POPULATION * weight
		estimated_people += people_in_timezone * eating_probability(local_hour)

	return int(estimated_people)


def estimated_people_sleeping_now(current_utc=None):
	if current_utc is None:
		current_utc = datetime.now(timezone.utc)

	estimated_people = 0

	for utc_offset, weight in TIMEZONE_WEIGHTS.items():
		local_time = current_utc + timedelta(hours=utc_offset)
		local_hour = local_time.hour + (local_time.minute / 60)
		people_in_timezone = WORLD_POPULATION * weight
		estimated_people += people_in_timezone * sleeping_probability(local_hour)

	return int(estimated_people)


people_eating_now = estimated_people_eating_now()
people_sleeping_now = estimated_people_sleeping_now()

print("Ciao a tutti")
print("Ma solo a quelli bravi")
print()
print("Stima simulata delle persone nel mondo che stanno mangiando ora:")
print(f"{people_eating_now:,}".replace(",", "."))
print()
print("Stima simulata delle persone nel mondo che stanno dormendo ora:")
print(f"{people_sleeping_now:,}".replace(",", "."))

