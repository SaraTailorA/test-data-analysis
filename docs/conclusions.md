# Conclusions and Business Insights

## Executive Summary

This project developed an end-to-end data pipeline for an e-commerce sales dataset, covering data extraction, transformation, validation, storage in PostgreSQL, and analysis through an interactive Power BI dashboard.

The dataset contains 5,000 sales records and 12 original columns, including information about orders, customers, products, regions, payment methods, delivery times, customer ratings, and revenue.

The analysis focuses on revenue performance, customer contribution, regional distribution, year-over-year variation, and the relationship between delivery time and customer satisfaction.

---

## Key Business Insights

### 1. Revenue Trend by Year

The annual revenue trend shows that revenue remained relatively high throughout most of the analyzed period, although there are noticeable fluctuations between years.

The final year, 2035, shows a significant decrease in revenue compared with the previous year. This variation should be considered when evaluating overall business performance and may require further investigation into the causes of the decline.

---

### 2. Top 5 Customers by Revenue

The Top 5 Customers analysis identifies the customers contributing the highest revenue to the business.

Customer **1663** is the highest contributor among the five customers displayed, followed by customers **1955, 1675, 1276, and 1647**.

Identifying high-value customers can support customer retention strategies and help prioritize efforts toward customers with greater revenue contribution.

---

### 3. Revenue Distribution by Region

Revenue is relatively balanced across the four regions:

| Region | Revenue Share |
|---|---:|
| West | 26.33% |
| North | 25.08% |
| South | 24.40% |
| East | 24.19% |

The **West** region has the highest revenue share at 26.33%, while the East has the lowest at 24.19%.

The difference between the regions is relatively small, indicating that revenue is not heavily concentrated in a single region.

---

### 4. Year-over-Year Revenue Growth

The Year-over-Year Revenue Growth analysis shows that revenue experienced both positive and negative variations across the analyzed years.

The most significant negative variation occurs in **2035**, where revenue decreases substantially compared with the previous year.

Year-over-year analysis provides a useful indicator for identifying periods of growth and decline and can help determine when additional business investigation is required.

---

### 5. Delivery Time vs. Customer Rating

The scatter plot compares average delivery time with average customer rating across customers.

The distribution of points does not show a strong or obvious linear relationship between delivery time and customer rating.

This suggests that delivery time alone may not be sufficient to explain differences in customer satisfaction. Other factors, such as region, product category, payment method, or other customer characteristics, could be analyzed in a deeper study.

---

## Overall Conclusion

The project demonstrates a complete data engineering and business intelligence workflow, from a raw Kaggle dataset to a validated analytical model in PostgreSQL and an interactive Power BI dashboard.

The resulting analysis provides visibility into revenue trends, high-value customers, regional performance, year-over-year changes, and customer satisfaction indicators.

The combination of ETL validation, a simple star schema, PostgreSQL storage, and Power BI visualization creates a reproducible foundation for future analysis and business decision-making.