// Mock Claude API endpoint for development
// In production, replace with actual Claude integration

export interface ClaudeCommand {
  command: string;
  explanation: string;
  risk_level: 'safe' | 'moderate' | 'dangerous';
}

const commands: ClaudeCommand[] = [
  {
    command: "ps aux | grep -E 'dawn|neuro' | awk '{print $2, $11}'",
    explanation: "Checking DAWN-related processes",
    risk_level: 'safe'
  },
  {
    command: "nvidia-smi --query-gpu=temperature.gpu,utilization.gpu,memory.used --format=csv,noheader",
    explanation: "Monitoring GPU status for neural processing",
    risk_level: 'safe'
  },
  {
    command: "top -b -n 1 | head -20",
    explanation: "Analyzing system resource usage",
    risk_level: 'safe'
  },
  {
    command: "journalctl -u dawn-cognitive --since '5 minutes ago' --no-pager",
    explanation: "Reviewing recent DAWN system logs",
    risk_level: 'safe'
  },
  {
    command: "netstat -tulpn | grep LISTEN",
    explanation: "Checking active network listeners",
    risk_level: 'moderate'
  }
];

export async function generateClaudeCommand(): Promise<ClaudeCommand> {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 500));
  
  // Return random command for demo
  return commands[Math.floor(Math.random() * commands.length)];
} 