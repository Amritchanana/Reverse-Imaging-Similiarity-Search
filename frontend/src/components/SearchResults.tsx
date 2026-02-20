import React from "react";

export interface SearchResult {
  id: string;
  imageUrl: string;
  similarity: number;
  label?: string;
  productId?: string;
}

interface SearchResultsProps {
  results: SearchResult[];
}

const getSimilarityClass = (score: number) => {
  if (score >= 0.8) return "result-card__similarity--high";
  if (score >= 0.5) return "result-card__similarity--medium";
  return "result-card__similarity--low";
};

const SearchResults: React.FC<SearchResultsProps> = ({ results }) => {
  if (results.length === 0) {
    return (
      <div className="empty-state">
        <svg viewBox="0 0 24 24">
          <circle cx="11" cy="11" r="8" />
          <line x1="21" y1="21" x2="16.65" y2="16.65" />
        </svg>
        <p>No similar images found. Try a different image.</p>
      </div>
    );
  }

  return (
    <div className="results">
      <div className="results__header">
        <h2 className="results__title">Similar Images</h2>
        <span className="results__count">{results.length} results</span>
      </div>
      <div className="results__grid">
        {results.map((result) => (
          <div key={result.id} className="result-card">
            <img
              className="result-card__image"
              src={result.imageUrl}
              alt={result.label || "Similar image"}
              loading="lazy"
            />
            <div className="result-card__footer">
              <p
                className={`result-card__similarity ${getSimilarityClass(result.similarity)}`}
              >
                {(result.similarity * 100).toFixed(1)}% match
              </p>
              {result.label && (
                <p className="result-card__label">{result.label}</p>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SearchResults;
