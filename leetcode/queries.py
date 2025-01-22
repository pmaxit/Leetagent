GET_USER_CONTESTS = """
query getUserContests($username: String!) {
  userContestRanking(username: $username) {
    attendedContestsCount
    rating
    globalRanking
  }
}
"""

GET_QUESTIONS = """
query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
  problemsetQuestionList: questionList(
    categorySlug: $categorySlug
    limit: $limit
    skip: $skip
    filters: $filters
  ) {
    total: totalNum
    questions: data {
      acRate
      difficulty
      freqBar
      frontendQuestionId: questionFrontendId
      isFavor
      paidOnly: isPaidOnly
      status
      title
      titleSlug
      topicTags {
        name
        id
        slug
      }
      hasSolution
      hasVideoSolution
    }
  }
}
"""

GET_PYTHON_SOLUTIONS = """
query ugcArticleSolutionArticles($questionSlug: String!, $orderBy: ArticleOrderByEnum, $userInput: String, $tagSlugs: [String!], $skip: Int, $before: String, $after: String, $first: Int, $last: Int, $isMine: Boolean) {
  ugcArticleSolutionArticles(
    questionSlug: $questionSlug
    orderBy: $orderBy
    userInput: $userInput
    tagSlugs: $tagSlugs
    skip: $skip
    first: $first
    before: $before
    after: $after
    last: $last
    isMine: $isMine
  ) {
    totalNum
    pageInfo {
      hasNextPage
    }
    edges {
      node {
        ...ugcSolutionArticleFragment
      }
    }
  }
}

fragment ugcSolutionArticleFragment on SolutionArticleNode {
  uuid
  title
  slug
  summary
  author {
    realName
    userAvatar
    userSlug
    userName
    nameColor
    certificationLevel
    activeBadge {
      icon
      displayName
    }
  }
  articleType
  thumbnail
  summary
  createdAt
  updatedAt
  status
  isLeetcode
  canSee
  canEdit
  isMyFavorite
  chargeType
  myReactionType
  topicId
  hitCount
  hasVideoArticle
  reactions {
    count
    reactionType
  }
  title
  slug
  tags {
    name
    slug
    tagType
  }
  topic {
    id
    topLevelCommentCount
  }
}
"""

GET_SOLUTION_DETAIL = """
query ugcArticleSolutionArticle($articleId: ID, $topicId: ID) {
  ugcArticleSolutionArticle(articleId: $articleId, topicId: $topicId) {
    ...ugcSolutionArticleFragment
    content
    isSerialized
    isArticleReviewer
    scoreInfo {
      scoreCoefficient
    }
    prev {
      uuid
      slug
      topicId
      title
    }
    next {
      uuid
      slug
      topicId
      title
    }
  }
}

fragment ugcSolutionArticleFragment on SolutionArticleNode {
  uuid
  title
  slug
  summary
  author {
    realName
    userAvatar
    userSlug
    userName
    nameColor
    certificationLevel
    activeBadge {
      icon
      displayName
    }
  }
  articleType
  thumbnail
  summary
  createdAt
  updatedAt
  status
  isLeetcode
  canSee
  canEdit
  isMyFavorite
  chargeType
  myReactionType
  topicId
  hitCount
  hasVideoArticle
  reactions {
    count
    reactionType
  }
  title
  slug
  tags {
    name
    slug
    tagType
  }
  topic {
    id
    topLevelCommentCount
  }
}
"""