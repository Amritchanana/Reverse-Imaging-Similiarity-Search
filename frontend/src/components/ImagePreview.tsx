import React from "react";

interface ImagePreviewProps {
  file: File;
  previewUrl: string;
  onSearch: () => void;
  onRemove: () => void;
  isSearching: boolean;
}

const formatSize = (bytes: number) => {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1048576) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / 1048576).toFixed(1)} MB`;
};

const ImagePreview: React.FC<ImagePreviewProps> = ({
  file,
  previewUrl,
  onSearch,
  onRemove,
  isSearching,
}) => {
  return (
    <div className="preview-card">
      <div className="preview-card__image-wrap">
        <img src={previewUrl} alt="Preview" />
      </div>
      <div className="preview-card__info">
        <p className="preview-card__name">{file.name}</p>
        <p className="preview-card__meta">
          {file.type.split("/")[1]?.toUpperCase()} · {formatSize(file.size)}
        </p>
        <div className="preview-card__actions">
          <button
            className="btn btn--primary"
            onClick={onSearch}
            disabled={isSearching}
          >
            <svg viewBox="0 0 24 24">
              <circle cx="11" cy="11" r="8" />
              <line x1="21" y1="21" x2="16.65" y2="16.65" />
            </svg>
            {isSearching ? "Searching..." : "Search"}
          </button>
          <button className="btn btn--ghost" onClick={onRemove}>
            <svg viewBox="0 0 24 24">
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
            Remove
          </button>
        </div>
      </div>
    </div>
  );
};

export default ImagePreview;
