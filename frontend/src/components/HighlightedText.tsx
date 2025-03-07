import React from 'react';

interface HighlightedTextProps {
  text: string;
  highlight: string;
}

function HighlightedText({ text, highlight }: HighlightedTextProps) {
  if (!highlight) return <>{text}</>;

  const regex = new RegExp(`(${highlight})`, 'gi');
  const parts = text.split(regex);

  return (
    <>
      {parts.map((part, index) => 
        regex.test(part) ? (
          <mark key={index}>{part}</mark>
        ) : (
          <span key={index}>{part}</span>
        )
      )}
    </>
  );
}

export default HighlightedText;