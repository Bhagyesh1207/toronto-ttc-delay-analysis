## Data quality audit

|   records | first_date   | last_date   |   positive_delay_records |   zero_minute_records |   observed_codes |   unmapped_code_records |
|----------:|:-------------|:------------|-------------------------:|----------------------:|-----------------:|------------------------:|
|     44664 | 2025-01-01   | 2026-08-31  |                    15800 |                 28864 |              138 |                    1493 |

## Line-level burden (not a per-rider rate)

| line   |   records |   positive_events |   total_minutes |   mean_positive_min |   share_of_minutes_pct |   burden_rank |
|:-------|----------:|------------------:|----------------:|--------------------:|-----------------------:|--------------:|
| Line 1 |     23134 |              8640 |           65506 |                7.58 |                   53.7 |             1 |
| Line 2 |     19758 |              6532 |           51508 |                7.89 |                   42.2 |             2 |
| Line 4 |      1772 |               628 |            4954 |                7.89 |                    4.1 |             3 |

## Most impacted stations (minimum 100 positive events)

| line   | station               |   positive_events |   total_minutes |   rank_in_line |
|:-------|:----------------------|------------------:|----------------:|---------------:|
| Line 1 | EGLINTON STATION      |               445 |            3998 |              1 |
| Line 2 | KIPLING STATION       |               577 |            3457 |              1 |
| Line 2 | KENNEDY BD STATION    |               533 |            3116 |              2 |
| Line 1 | SHEPPARD WEST STATION |               257 |            3096 |              2 |
| Line 2 | VICTORIA PARK STATION |               263 |            3094 |              3 |
| Line 1 | WILSON STATION        |               512 |            3073 |              3 |
| Line 1 | BLOOR STATION         |               504 |            2848 |              4 |
| Line 1 | FINCH STATION         |               464 |            2771 |              5 |
| Line 1 | LAWRENCE STATION      |               243 |            2324 |              6 |
| Line 1 | DAVISVILLE STATION    |               336 |            2289 |              7 |
| Line 2 | YONGE BD STATION      |               322 |            2222 |              4 |
| Line 1 | ST CLAIR WEST STATION |               230 |            2176 |              8 |

## Top coded reasons among positive-delay records

| code   | reason                                      |   positive_events |   total_minutes |   mean_minutes |
|:-------|:--------------------------------------------|------------------:|----------------:|---------------:|
| SUDP   | DISORDERLY PATRON                           |              1916 |           12103 |            6.3 |
| MUIR   | INJURED/ILL CUSTOMER ON TRAIN â MEDICAL AID REFUSED                                             |              1216 |            8501 |            7   |
| SUUT   | UNAUTHORIZED AT TRACK LEVEL                 |               533 |            6416 |           12   |
| SUO    | SECURITY OTHER                              |               740 |            6305 |            8.5 |
| MUI    | INJURED/ILL CUSTOMER ON TRAIN â TRANSPORTED                                             |               535 |            5862 |           11   |
| MUPAA  | PAA â NO TROUBLE FOUND                                             |              1293 |            5393 |            4.2 |
| PUOPO  | OPTO (COMMUNICATIONS) TRAIN DOOR MONITORING |              1093 |            5369 |            4.9 |
| MUWEA  | WEATHER REPORTS / RELATED PROBLEMS          |               293 |            4820 |           16.5 |
| PUTIS  | ICE/SNOW RELATED PROBLEM                    |                60 |            4127 |           68.8 |
| TUO    | TRANSPORTATION OTHER                        |               582 |            3382 |            5.8 |
| PUTWZ  | WORK ZONES PROBLEMS â TRACK                                             |               292 |            3284 |           11.2 |
| MUSAN  | UNSANITARY VEHICLE                          |               712 |            3075 |            4.3 |

## Peak vs off-peak (record counts, not service-normalized risk)

| period          |   records |   positive_events |   total_minutes |   positive_share_pct |
|:----------------|----------:|------------------:|----------------:|---------------------:|
| 07-09 and 16-18 |     14144 |              5297 |           38455 |                 37.5 |
| other hours     |     30520 |             10503 |           83513 |                 34.4 |

## Monthly trends, same months year-over-year

|   year |   month |   positive_events |   minutes |   prior_year_same_month_minutes |   yoy_change_pct |
|-------:|--------:|------------------:|----------:|--------------------------------:|-----------------:|
|   2025 |      01 |               808 |      6381 |                             nan |            nan   |
|   2025 |      02 |               917 |      8766 |                             nan |            nan   |
|   2025 |      03 |               801 |      6305 |                             nan |            nan   |
|   2025 |      04 |               750 |      6052 |                             nan |            nan   |
|   2025 |      05 |               731 |      5432 |                             nan |            nan   |
|   2025 |      06 |               664 |      5117 |                             nan |            nan   |
|   2025 |      07 |               688 |      5597 |                             nan |            nan   |
|   2025 |      08 |               741 |      5127 |                             nan |            nan   |
|   2025 |      09 |               613 |      4179 |                             nan |            nan   |
|   2025 |      10 |               704 |      5150 |                             nan |            nan   |
|   2025 |      11 |               834 |      6187 |                             nan |            nan   |
|   2025 |      12 |               842 |      6458 |                             nan |            nan   |
|   2026 |      01 |               993 |     12366 |                            6381 |             93.8 |
|   2026 |      02 |               749 |      5816 |                            8766 |            -33.7 |
|   2026 |      03 |               834 |      5789 |                            6305 |             -8.2 |
|   2026 |      04 |               891 |      7167 |                            6052 |             18.4 |
|   2026 |      05 |               865 |      5612 |                            5432 |              3.3 |
|   2026 |      06 |               875 |      5538 |                            5117 |              8.2 |
|   2026 |      07 |               822 |      4782 |                            5597 |            -14.6 |
|   2026 |      08 |               678 |      4147 |                            5127 |            -19.1 |
