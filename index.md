---
layout: default
---

<!-- Text can be **bold**, _italic_, or ~~strikethrough~~. -->

<!-- [Link to another page](./another-page.html). -->

<!-- There should be whitespace between paragraphs.

There should be whitespace between paragraphs. We recommend including a README, or a file with information about your project. -->

# Introduction


In the realm of stock portfolio management, the application of advanced machine learning (ML) techniques for effective diversification is gaining traction. Our project aims to explore and leverage advanced ML models to categorize stock based on both textual description and financial data and give users an objective measure of their portfolio’s diversity. Recent studies have delved into clustering algorithms like Gaussian Mixture Models (GMM) for categorizing stocks. However, the potential of more advanced ML models in combination with clustering algorithms is still in its infancy.

# Problem Definition

The primary motivation is to overcome the shortcomings of conventional portfolio diversification and make a new and objective rating system for a portfolio's diversity. An article by Gilles Koumou investigates the utility of several common diversification practices and clears up several misconceptions, noting that “as the 2007–2009 financial crisis revealed, the concept remains misunderstood” <cite>(Koumou, 2020)</cite>. The project seeks to incorporate a nuanced understanding of stock types, utilizing features such as market capitalization, volatility, and textual information from company descriptions. Evidence-based studies on diversification practices, such as Koumou’s publication, will be considered throughout the duration of our project. The goal is to offer users a personalized and dynamically optimized portfolio aligned with individual preferences and market conditions.


# Results and Discussion

Based on the data, we have determined that the optimal number of clusters is 5 and have created a working diversity calculator for any number of sample portfolios. To test the model, we can test our model against various portfolios (High Diversity vs Low Diversity). The following portfolios are High Diversity portfolios, as they consist of various industries and spread out overall value.

| head1        | head two          | three |
|:-------------|:------------------|:------|
| ok           | good swedish fish | nice  |
| out of stock | good and plenty   | nice  |
| ok           | good `oreos`      | hmm   |
| ok           | good `zoute` drop | yumm  |


# Methods

We plan to employ a Gaussian Mixture Model (GMM) to determine if a stock portfolio is diversified through a diversification index, as GMM allows for flexible modeling of the stock market <cite>(Luxenberg & Boyd, 2023)</cite>. In order to feed the GMM, we will need feature vectors of the stocks in the dataset. We will formulate a description of each stock and pass it through an NLP model, like Word2Vec, to get the feature vectors. The GMM will output a vector of probabilities representing the stock's categorization. The original model's aggregation process remains intact, creating a "portfolio diversity" model. Then, for each stock in a portfolio, we will feed the vector into our model and multiplied by its respective weight in the user's original portfolio, reflecting the percentage of their investment in each stock. Theoretically, a more diverse portfolio is indicated by a closer alignment of values in the vector. We will utilize internal validation metrics like Silhouette score Davies-Bouldin index to optimize our model and external validation methods, as defined in the next section, to assess model performance <cite>(Wang, 2022)</cite>. Metrics related to portfolio diversity and alignment with user preferences will be considered.

# Potential Results and Discussion

The results of our model will be a more comprehensive representation of the diversity of users’ stock portfolio. It is expected that the outcomes improve portfolio diversity assessment. Discussion will focus on result implications, potential refinements, and the model's generalizability to broader financial markets. We will discuss the effectiveness of our representation by checking whether the investment that is diverse in our model shows the capability to be risk-tolerant while delivering a satisfactory return.

# Timeline and Contributions

Please go to this [link](https://docs.google.com/spreadsheets/d/14tqgJGyeV8g7UURRkbnhb-IWGrCUOo9_/edit?usp=sharing&ouid=117826216135502018457&rtpof=true&sd=true) to access the proposed timeline and contribution table.

# Checkpoint

As we will be using NLP and GMM to create our diversity model, this would in fact be a Machine Learning project. We will use the following datasets and APIs:
1. [Dataset for company name, size, and industry](https://www.kaggle.com/datasets/peopledatalabssf/free-7-million-company-dataset)
2. [Dataset for volume](https://www.kaggle.com/datasets/paultimothymooney/stock-market-data/data) 
3. [API for volatility score](https://www.alphaquery.com/stock/MSFT/volatility-option-statistics/30-day/historical-volatility)
4. [API for the market cap](https://site.financialmodelingprep.com/developer/docs/market-capitalization-api/?direct=true)

# References

<cite>
Koumou, G. B. (2020, June 4). Diversification and portfolio theory: a review. Financial Markets and Portfolio Management, 34, 267–312.
</cite>

<cite>
Luxenberg, E., & Boyd, S. (2023). Portfolio construction with gaussian mixture returns and exponential utility via convex optimization. Optimization and Engineering. https://doi.org/10.1007/s11081-023-09814-y
</cite>

<cite>
Wang Y, Grani A. Hanasusanto, Chin Pang Ho. (2022, July 7). Optimization online. Optimization Online. https://optimization-online.org/2022/07/8979/ 
</cite>


<!-- ## Header 2

> This is a blockquote following a header.
>
> When something is important enough, you do it even if the odds are not in your favor.

### Header 3

```js
// Javascript code with syntax highlighting.
var fun = function lang(l) {
  dateformat.i18n = require('./lang/' + l)
  return true;
}
```

```ruby
# Ruby code with syntax highlighting
GitHubPages::Dependencies.gems.each do |gem, version|
  s.add_dependency(gem, "= #{version}")
end
```

#### Header 4

*   This is an unordered list following a header.
*   This is an unordered list following a header.
*   This is an unordered list following a header.

##### Header 5

1.  This is an ordered list following a header.
2.  This is an ordered list following a header.
3.  This is an ordered list following a header.

###### Header 6

| head1        | head two          | three |
|:-------------|:------------------|:------|
| ok           | good swedish fish | nice  |
| out of stock | good and plenty   | nice  |
| ok           | good `oreos`      | hmm   |
| ok           | good `zoute` drop | yumm  |

### There's a horizontal rule below this.

* * *

### Here is an unordered list:

*   Item foo
*   Item bar
*   Item baz
*   Item zip

### And an ordered list:

1.  Item one
1.  Item two
1.  Item three
1.  Item four

### And a nested list:

- level 1 item
  - level 2 item
  - level 2 item
    - level 3 item
    - level 3 item
- level 1 item
  - level 2 item
  - level 2 item
  - level 2 item
- level 1 item
  - level 2 item
  - level 2 item
- level 1 item

### Small image

![Octocat](https://github.githubassets.com/images/icons/emoji/octocat.png)

### Large image

![Branching](https://guides.github.com/activities/hello-world/branching.png)


### Definition lists can be used with HTML syntax.

<dl>
<dt>Name</dt>
<dd>Godzilla</dd>
<dt>Born</dt>
<dd>1952</dd>
<dt>Birthplace</dt>
<dd>Japan</dd>
<dt>Color</dt>
<dd>Green</dd>
</dl> -->

<!-- ```
Long, single-line code blocks should not wrap. They should horizontally scroll if they are too long. This line should be long enough to demonstrate this.
```

```
The final element.
``` -->
