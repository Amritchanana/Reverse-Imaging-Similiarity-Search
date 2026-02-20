import { useState, useCallback } from "react";
import ImageUploader from "../components/ImageUploader";
import ImagePreview from "../components/ImagePreview";
import SearchResults, { SearchResult } from "../components/SearchResults";
import { searchImage } from "../api/searchApi";
import "../styles/search.css";

const Index: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string>("");
  const [isSearching, setIsSearching] = useState(false);
  const [results, setResults] = useState<SearchResult[] | null>(null);

  const handleImageSelect = useCallback((file: File) => {
    setSelectedFile(file);
    setPreviewUrl(URL.createObjectURL(file));
    setResults(null);
  }, []);

  const handleRemove = useCallback(() => {
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    setSelectedFile(null);
    setPreviewUrl("");
    setResults(null);
  }, [previewUrl]);

  const handleSearch = useCallback(async () => {
    if (!selectedFile) return;
    setIsSearching(true);
    setResults(null);

    try {
      const data = await searchImage(selectedFile);
      console.log("API Response:", data);

      const mapped: SearchResult[] = (data.results || []).map(
        (item: any, i: number) => {
          console.log("Mapping item:", item);
          return {
            id: item.product_id || String(i),
            imageUrl: item.image_url || "",
            similarity: item.Score || 0,
            label: item.product_id ? `Product ${item.product_id}` : "",
            productId: item.product_id || "",
          };
        }
      );

      console.log("Mapped results:", mapped);
      setResults(mapped);
    } catch (err) {
      console.error("Search error:", err);
      setResults([]);
    } finally {
      setIsSearching(false);
    }
  }, [selectedFile]);

  return (
    <div className="search-app">
      <header className="search-app__header">
        <h1 className="search-app__title">
          Reverse <span>Image Search</span>
        </h1>
        <p className="search-app__subtitle">
          Upload an image to find visually similar matches
        </p>
      </header>

      <main className="search-app__content">
        {!selectedFile && <ImageUploader onImageSelect={handleImageSelect} />}

        {selectedFile && previewUrl && (
          <ImagePreview
            file={selectedFile}
            previewUrl={previewUrl}
            onSearch={handleSearch}
            onRemove={handleRemove}
            isSearching={isSearching}
          />
        )}

        {isSearching && (
          <div className="loading">
            <div className="loading__spinner" />
            <p className="loading__text">Finding similar images…</p>
          </div>
        )}

        {results !== null && !isSearching && (
          <SearchResults results={results} />
        )}
      </main>
    </div>
  );
};

export default Index;
