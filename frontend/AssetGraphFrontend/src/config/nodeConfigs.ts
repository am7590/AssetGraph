interface NodeConfig {
  label: string;
  params?: Record<string, {
    type: string;
    default: any;
    field: string;
  }>;
}

export const NODE_CONFIGS: Record<string, NodeConfig> = {
  LoadTickerData: {
    label: 'Load Ticker Data',
    params: {
      ticker: { type: 'string', default: '', field: 'Ticker Symbol' },
      start_date: { type: 'string', default: '', field: 'Start Date' },
      end_date: { type: 'string', default: '', field: 'End Date' }
    }
  },
  CalculateMovingAverage: {
    label: 'Calculate Moving Average',
    params: {
      window_size: { type: 'number', default: 20, field: 'Window Size' },
      column: { type: 'string', default: 'close', field: 'Column Name' }
    }
  },
  CalculateRSI: {
    label: 'Calculate RSI',
    params: {
      period: { type: 'number', default: 14, field: 'Period' },
      column: { type: 'string', default: 'close', field: 'Column Name' }
    }
  },
  CalculateMACD: {
    label: 'Calculate MACD',
    params: {
      fast_period: { type: 'number', default: 12, field: 'Fast Period' },
      slow_period: { type: 'number', default: 26, field: 'Slow Period' },
      signal_period: { type: 'number', default: 9, field: 'Signal Period' },
      column: { type: 'string', default: 'close', field: 'Column Name' }
    }
  },
  Load10K: {
    label: 'Load 10K',
    params: {
      ticker: { type: 'string', default: '', field: 'Ticker Symbol' },
      year: { type: 'number', default: new Date().getFullYear(), field: 'Year' }
    }
  },
  Summarize10K: {
    label: 'Summarize 10K',
    params: {
      section: { type: 'string', default: '', field: 'Section' },
      max_length: { type: 'number', default: 1000, field: 'Max Length' }
    }
  },
  LoadIncomeStatement: {
    label: 'Load Income Statement',
    params: {
      period: { type: 'string', default: 'annual', field: 'Period' },
      limit: { type: 'number', default: 10, field: 'Limit' }
    }
  },
  LoadBalanceSheet: {
    label: 'Load Balance Sheet',
    params: {
      period: { type: 'string', default: 'annual', field: 'Period' },
      limit: { type: 'number', default: 10, field: 'Limit' }
    }
  },
  LoadCashFlow: {
    label: 'Load Cash Flow',
    params: {
      period: { type: 'string', default: 'annual', field: 'Period' },
      limit: { type: 'number', default: 10, field: 'Limit' }
    }
  },
  PreprocessFinancials: {
    label: 'Preprocess Financials'
  },
  SummarizeIncomeStatement: {
    label: 'Summarize Income Statement'
  },
  GenerateLLMReport: {
    label: 'Generate LLM Report',
    params: {
      report_type: { type: 'string', default: 'full', field: 'Report Type' }
    }
  }
}; 