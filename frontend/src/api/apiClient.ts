// API client for the law bot application

export interface SavedQuery {
  id: string;
  queryText: string;
  name?: string;
}

export interface LegalIssue {
  id: string;
  name: string;
}

export interface CourtRuling {
  id: string;
  title: string;
  date: string;
  court: string;
  issues: string[];
  defaultDisplayView: string;
  displayViews: {
    [key: string]: string;
  };
}

export interface QueryResults {
  rulings: CourtRuling[];
  legalIssues: string[];
  availableDisplayViews: string[];
}

// Mock data for development
const mockSavedQueries: SavedQuery[] = [
  { id: '1', queryText: 'Copyright infringement in digital media', name: 'Copyright Case' },
  { id: '2', queryText: 'Contract breach damages calculation' },
  { id: '3', queryText: 'Patent validity requirements', name: 'Patent Research' },
];

const mockQueryResults: QueryResults = {
  rulings: [
    {
      id: '1',
      title: 'Doe v. Tech Corp',
      date: '2023-05-15',
      court: 'Supreme Court',
      issues: ['Copyright', 'Digital Media'],
      defaultDisplayView: 'Summary',
      displayViews: {
        'Summary': 'This ruling established that AI-generated content cannot be copyrighted without substantial human creative input.',
        'Key Factors': 'The court considered: 1) level of human guidance, 2) originality of prompts, 3) randomness of output.',
        'Legal Precedent': 'Builds on Smith v. Software Inc. (2018) which began addressing digital creative works.',
      },
    },
    {
      id: '2',
      title: 'State v. Neural Networks Ltd',
      date: '2024-01-22',
      court: 'Circuit Court of Appeals',
      issues: ['Data Privacy', 'AI Training'],
      defaultDisplayView: 'Summary',
      displayViews: {
        'Summary': 'Court ruled that using publicly available data for AI training constitutes fair use, but with limitations.',
        'Key Factors': 'Factors considered: 1) commercial nature of use, 2) impact on potential markets, 3) amount of data used.',
        'Legal Precedent': 'Distinguished from earlier cases by focusing on transformative nature of the AI training process.',
      },
    },
    {
      id: '3',
      title: 'Creative Guild v. Generative Systems',
      date: '2023-11-08',
      court: 'Federal Court',
      issues: ['Copyright', 'AI Authorship'],
      defaultDisplayView: 'Key Factors',
      displayViews: {
        'Summary': 'Determined that AI systems cannot be listed as inventors on patents, but can be tools for human inventors.',
        'Key Factors': 'Court examined: 1) meaning of "inventor" in statute, 2) nature of conception, 3) public policy considerations.',
        'Legal Precedent': 'Follows international precedent set in European and Australian courts during 2022-2023.',
      },
    },
  ],
  legalIssues: ['Copyright', 'Digital Media', 'Data Privacy', 'AI Training', 'AI Authorship'],
  availableDisplayViews: ['Summary', 'Key Factors', 'Legal Precedent'],
};

// API client for making requests
const apiClient = {
  // Get saved queries from the server
  getSavedQueries: async (): Promise<SavedQuery[]> => {
    // In a real app, this would be a fetch call
    // return fetch('/api/savedQueries').then(res => res.json());
    
    // For development, return mock data
    return new Promise(resolve => {
      setTimeout(() => resolve(mockSavedQueries), 500);
    });
  },

  // Fetch legal rulings based on a query
  fetchLegalRulings: async (query: string): Promise<QueryResults> => {
    // In a real app, this would be a fetch call
    // return fetch(`/api/rulings?query=${encodeURIComponent(query)}`).then(res => res.json());
    
    // For development, return mock data with small delay to simulate API call
    return new Promise(resolve => {
      setTimeout(() => resolve(mockQueryResults), 800);
    });
  },
};

export default apiClient;