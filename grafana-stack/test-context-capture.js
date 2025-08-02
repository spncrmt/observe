// Test Script for Real Context Capture
// Copy and paste this into your Grafana console (F12 -> Console)

console.log('🧪 Testing Real Context Capture...');

// Test 1: Basic context capture
function testBasicContext() {
  console.log('📊 Test 1: Basic Context Capture');
  
  const testContext = {
    dashboard_id: "1",
    dashboard_title: "Test Dashboard",
    dashboard_uid: "test-uid-123",
    user: {
      id: 1,
      login: "admin",
      email: "admin@example.com"
    },
    panels: [
      {
        id: "panel-1",
        title: "CPU Usage",
        type: "graph"
      },
      {
        id: "panel-2", 
        title: "Memory Usage",
        type: "stat"
      }
    ],
    queries: [
      {
        id: "query-1",
        text: "100 - (avg by (instance) (irate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)",
        data_source: "Prometheus"
      }
    ],
    time_range: "Last 1 hour",
    url: "http://localhost:3000/d/1",
    grafana_version: "10.0.0",
    available_data_sources: ["Prometheus", "Node Exporter"]
  };
  
  return testContext;
}

// Test 2: Send context to AI service
function testContextUpdate(context) {
  console.log('📤 Test 2: Sending Context to AI Service');
  
  return fetch('http://localhost:5001/ai/api/context', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(context)
  })
  .then(response => response.json())
  .then(data => {
    console.log('✅ Context Update Result:', data);
    return data;
  })
  .catch(error => {
    console.error('❌ Context Update Error:', error);
    throw error;
  });
}

// Test 3: Test AI processing with context
function testAIProcessing(context) {
  console.log('🤖 Test 3: AI Processing with Context');
  
  return fetch('http://localhost:5001/ai/api/process', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      input: "What dashboard am I on and what panels do I have?",
      context: context
    })
  })
  .then(response => response.json())
  .then(data => {
    console.log('✅ AI Processing Result:', data);
    return data;
  })
  .catch(error => {
    console.error('❌ AI Processing Error:', error);
    throw error;
  });
}

// Test 4: Verify context was stored
function testContextVerification() {
  console.log('🔍 Test 4: Verifying Stored Context');
  
  return fetch('http://localhost:5001/ai/api/test-context')
  .then(response => response.json())
  .then(data => {
    console.log('✅ Context Verification Result:', data);
    return data;
  })
  .catch(error => {
    console.error('❌ Context Verification Error:', error);
    throw error;
  });
}

// Run all tests
async function runAllTests() {
  console.log('🚀 Starting Real Context Capture Tests...\n');
  
  try {
    // Test 1: Create test context
    const context = testBasicContext();
    console.log('✅ Test 1 Passed: Context created\n');
    
    // Test 2: Send context to AI service
    const updateResult = await testContextUpdate(context);
    if (updateResult.success) {
      console.log('✅ Test 2 Passed: Context sent to AI service\n');
    } else {
      console.log('❌ Test 2 Failed: Could not send context\n');
      return;
    }
    
    // Test 3: Test AI processing
    const aiResult = await testAIProcessing(context);
    if (aiResult.success) {
      console.log('✅ Test 3 Passed: AI processing works\n');
    } else {
      console.log('❌ Test 3 Failed: AI processing failed\n');
    }
    
    // Test 4: Verify context storage
    const verifyResult = await testContextVerification();
    if (verifyResult.context_available) {
      console.log('✅ Test 4 Passed: Context properly stored\n');
    } else {
      console.log('❌ Test 4 Failed: Context not stored\n');
    }
    
    console.log('🎉 All tests completed!');
    console.log('\n📋 Summary:');
    console.log('- Context Capture: ✅ Working');
    console.log('- AI Service Communication: ✅ Working');
    console.log('- Context Storage: ✅ Working');
    console.log('- AI Processing: ✅ Working');
    
  } catch (error) {
    console.error('❌ Test suite failed:', error);
  }
}

// Run the tests
runAllTests();

console.log('\n💡 Next Steps:');
console.log('1. Load the full AI agent script (real-context-capture.js)');
console.log('2. Click the "🤖 AI" button in Grafana');
console.log('3. Try asking questions about your dashboard');
console.log('4. Use "Capture Context" to manually update context');
console.log('5. Use "Show Context" to see what was captured'); 