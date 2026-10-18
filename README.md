# senate-data

Stock trades reported by U.S. senators, scraped once a day from the Senate's
official disclosure site ([efdsearch.senate.gov](https://efdsearch.senate.gov))
and published as one CSV: [`senate_trades.csv`](senate_trades.csv).

It runs on GitHub Actions because the Senate site only answers connections
from the U.S. XYZ Terminal downloads the CSV and shows the trades as news.

- Amounts are the dollar ranges senators file, never exact figures.
- `link` is the path of the official filing on efdsearch.senate.gov.
- `tkr` is the ticker as filed, or one read from the asset name when the
  filing left it blank (`tkr_recovered` is true for those).

The scraper is copied from [Quantgress](https://github.com/DMulajkar/Quantgress)
(MIT, see [LICENSE](LICENSE)).

Federal law (5 U.S.C. § 13107(c)) makes it unlawful to use these reports for a
commercial purpose other than by news and communications media for
dissemination to the general public, for credit ratings, or for soliciting
money.
