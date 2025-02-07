# Book Recommendation System (Hybrid Approach)

## Introduction
This project implements a book recommendation system using a Hybrid Approach that combines Collaborative Filtering and Content-Based Filtering. The goal is to provide personalized book suggestions based on user preferences and reading history.

## Concept Explanation
- **Collaborative Filtering:** Suggests books based on user interactions, identifying similar users and recommending books they liked.
- **Content-Based Filtering:** Uses book attributes (title, author, description) to find similar books to those a user has liked.
- **Hybrid Approach:** Combines both methods to improve recommendation accuracy by leveraging their strengths.

## Implementation
### Pipeline
![Screenshot 2025-02-07 223823](https://github.com/user-attachments/assets/d69ab50f-968c-4c12-adfe-9482089def6e)

### Data
- Kaggle: https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset

### Model
#### Content Based
- **Bags of words** is all attributes of a book join together.
- **TF-IDF** is used to convert book 'bags of words' into vector representations for Content-Based Filtering.
- **Cosine Similarity** measures book similarity.

#### Collaborative Filtering
- Normalize pivot table of user and item
![image](https://github.com/user-attachments/assets/ec7ca8ca-955f-4c3f-8840-262028791da7)
link: https://machinelearningcoban.com/2017/05/24/collaborativefiltering/


- Create user similar matrix by cosine similarity and use K Nearest Neighbor to get result
## Product
![Screenshot 2025-02-07 224007](https://github.com/user-attachments/assets/89b246c4-b3d2-44e4-a6d8-caf9fddf6e99)
