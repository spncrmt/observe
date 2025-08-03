# Manual Dashboard Setup Guide

## Problem
Grafana is having trouble parsing complex PromQL queries with nested calculations. The error suggests it's trying to parse the query as a regex pattern instead of PromQL.

## Solution: Manual Dashboard Creation

### Step 1: Create New Dashboard
1. Go to http://localhost:3000
2. Click **+** → **Dashboard**
3. Click **"Add visualization"**

### Step 2: Add CPU Panel
1. **Data Source**: Select "Prometheus"
2. **Query**: Copy and paste this exact query:
   ```
   rate(node_cpu_seconds_total{mode="idle"}[5m]) * 100
   ```
3. **Title**: "CPU Idle %"
4. **Unit**: percent
5. **Click "Run Query"** to test
6. **Click "Apply"** to save the panel

### Step 3: Add Memory Panel
1. **Click "Add visualization"** again
2. **Data Source**: Select "Prometheus"
3. **Query**: Copy and paste this exact query:
   ```
   node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes * 100
   ```
4. **Title**: "Memory Available %"
5. **Unit**: percent
6. **Click "Run Query"** to test
7. **Click "Apply"** to save the panel

### Step 4: Add System Load Panel
1. **Click "Add visualization"** again
2. **Data Source**: Select "Prometheus"
3. **Query**: Copy and paste this exact query:
   ```
   node_load1
   ```
4. **Title**: "System Load (1m)"
5. **Click "Run Query"** to test
6. **Click "Apply"** to save the panel

### Step 5: Add Service Health Panel
1. **Click "Add visualization"** again
2. **Data Source**: Select "Prometheus"
3. **Query**: Copy and paste this exact query:
   ```
   up
   ```
4. **Title**: "Service Health"
5. **Visualization Type**: Change to "Stat"
6. **Click "Run Query"** to test
7. **Click "Apply"** to save the panel

### Step 6: Save Dashboard
1. **Click "Save dashboard"** (top right)
2. **Dashboard name**: "Manual System Dashboard"
3. **Click "Save"**

## Alternative: Import Simple Dashboard
If manual creation doesn't work, try importing the `simple-working-dashboard.json` file:
1. Go to http://localhost:3000
2. Click **+** → **Import**
3. Upload `simple-working-dashboard.json`
4. Click **Import**

## Working Queries (Tested)
These queries have been tested and work with the Prometheus API:

```promql
# CPU Idle Percentage
rate(node_cpu_seconds_total{mode="idle"}[5m]) * 100

# Memory Available Percentage  
node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes * 100

# System Load (1 minute)
node_load1

# Service Health
up
```

## Troubleshooting
- If queries still fail, try removing the quotes around "idle" in the CPU query
- Make sure the time range is set to "Last 15 minutes"
- Check that Prometheus data source is properly configured
- Verify that Node Exporter is running and collecting data 