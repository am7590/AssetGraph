export interface ParameterSchema {
  name: string;
  type: 'string' | 'number' | 'boolean';
  required: boolean;
  default?: any;
  validation?: (value: any) => boolean;
}

export const NODE_PARAMETER_SCHEMAS: Record<string, ParameterSchema[]> = {
  'load_ticker_data': [
    { name: 'ticker', type: 'string', required: true },
    { name: 'start_date', type: 'string', required: false },
    { name: 'end_date', type: 'string', required: false }
  ],
  'load_income_statement': [
    { name: 'period', type: 'string', required: false, default: 'annual' },
    { name: 'limit', type: 'number', required: false, default: 10 }
  ],
  'load_balance_sheet': [
    { name: 'period', type: 'string', required: false, default: 'annual' },
    { name: 'limit', type: 'number', required: false, default: 10 }
  ],
  'load_cash_flow': [
    { name: 'period', type: 'string', required: false, default: 'annual' },
    { name: 'limit', type: 'number', required: false, default: 10 }
  ],
  'preprocess_financials': [],
  'summarize_income_statement': [],
  'generate_llm_report': [
    { name: 'report_type', type: 'string', required: false, default: 'full' }
  ]
}; 