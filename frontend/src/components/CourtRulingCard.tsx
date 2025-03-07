import React from 'react';
import HighlightedText from './HighlightedText';
import { CourtRuling } from '../api/apiClient';

interface CourtRulingCardProps {
  ruling: CourtRuling;
  activeDisplayView: string;
  keywordFilter: string;
}

function CourtRulingCard({ ruling, activeDisplayView, keywordFilter }: CourtRulingCardProps) {
  const textContent = ruling.displayViews[activeDisplayView] || '';

  return (
    <div className="court-ruling-card">
      <h3>{ruling.title}</h3>
      <div className="court-ruling-meta">
        <span>{ruling.court}</span> | <span>{ruling.date}</span>
      </div>
      <div className="court-ruling-content">
        <HighlightedText text={textContent} highlight={keywordFilter} />
      </div>
      <div className="fade-out-overlay" />
    </div>
  );
}

export default CourtRulingCard;