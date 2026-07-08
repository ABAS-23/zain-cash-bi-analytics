from google_play_scraper import Sort, reviews
import csv
import os

APP_ID = "mobi.foo.zaincash"
OUTPUT_FILE = "zaincash_reviews.csv"

def scrape_all_reviews():
    all_reviews = []
    continuation_token = None
    batch = 1

    print(" بدء جمع تقييمات ZainCash...")
    print("-" * 50)

    while True:
        try:
            result, continuation_token = reviews(
                APP_ID,
                lang="ar",
                country="iq",
                sort=Sort.NEWEST,
                count=200,
                continuation_token=continuation_token
            )

            if not result:
                print(" لا توجد تقييمات إضافية، اكتمل الجمع.")
                break

            all_reviews.extend(result)
            print(f" الدفعة {batch}: تم جلب {len(result)} تقييم | الإجمالي: {len(all_reviews)}")
            batch += 1

            if continuation_token is None:
                print(" وصلنا لآخر تقييم متاح.")
                break

        except Exception as e:
            print(f" خطأ: {e}")
            break

    return all_reviews


def save_to_csv(reviews_list):
    if not reviews_list:
        print(" لا توجد بيانات للحفظ.")
        return

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["الاسم", "التقييم", "التاريخ", "التعليق", "الإعجابات"])

        for r in reviews_list:
            writer.writerow([
                r.get("userName", ""),
                r.get("score", ""),
                r.get("at", "").strftime("%Y-%m-%d") if r.get("at") else "",
                r.get("content", "").replace("\n", " "),
                r.get("thumbsUpCount", 0),
            ])

    print("-" * 50)
    print(f" تم الحفظ في: {os.path.abspath(OUTPUT_FILE)}")
    print(f" إجمالي التقييمات المحفوظة: {len(reviews_list)}")


if __name__ == "__main__":
    data = scrape_all_reviews()
    save_to_csv(data)