import React from 'react';
import CourtRulingCard from './CourtRulingCard';
import { CourtRuling } from '../api/apiClient';

interface CourtRulingListProps {
  rulings: CourtRuling[];
  selectedDisplayView: string | null;
  keywordFilter: string;
}

function CourtRulingList({ rulings, selectedDisplayView, keywordFilter }: CourtRulingListProps) {
  return (
    <div className="court-ruling-list">
      <h3>{rulings.length} documents matched</h3>
      {rulings.map(ruling => (
        <CourtRulingCard
          key={ruling.id}
          ruling={ruling}
          activeDisplayView={selectedDisplayView || ruling.defaultDisplayView}
          keywordFilter={keywordFilter}
        />
      ))}
    </div>
  );
}

export default CourtRulingList;