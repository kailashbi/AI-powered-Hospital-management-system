import React, { useState, useEffect } from 'react';
import { kafkaService } from '../../services/kafkaService';
import {
  Radio,
  Activity,
  Zap,
  AlertTriangle,
  RefreshCw,
  Send,
  CheckCircle2,
  Server,
  Layers,
  Database,
  Terminal,
  Play
} from 'lucide-react';

export const AdminKafkaStream = () => {
  const [kafkaStatus, setKafkaStatus] = useState(null);
  const [events, setEvents] = useState([]);
  const [selectedTopic, setSelectedTopic] = useState('');
  const [loading, setLoading] = useState(true);
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [publishing, setPublishing] = useState(false);
  const [publishSuccess, setPublishSuccess] = useState('');

  // Manual Publisher State
  const [testTopic, setTestTopic] = useState('kaire-vitals-stream');
  const [testEventType, setTestEventType] = useState('VITAL_RECORDED');
  const [testPayloadStr, setTestPayloadStr] = useState(
    JSON.stringify(
      {
        patient_id: 1,
        vitals: { temperature: 101.2, heart_rate: 124, blood_pressure: '165/105', spo2: 92 },
        notes: 'Simulated real-time patient vital sign stream event',
      },
      null,
      2
    )
  );

  const fetchKafkaData = async () => {
    try {
      const statusRes = await kafkaService.getStatus();
      setKafkaStatus(statusRes.kafka);

      const eventsRes = await kafkaService.getEvents(selectedTopic || null, 50);
      setEvents(eventsRes.events || []);
    } catch (err) {
      console.error('Failed to fetch Kafka stream data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchKafkaData();
  }, [selectedTopic]);

  useEffect(() => {
    let interval;
    if (autoRefresh) {
      interval = setInterval(() => {
        fetchKafkaData();
      }, 3000);
    }
    return () => clearInterval(interval);
  }, [autoRefresh, selectedTopic]);

  const handlePublishTestEvent = async (e) => {
    e.preventDefault();
    setPublishing(true);
    setPublishSuccess('');
    try {
      let parsedPayload = {};
      try {
        parsedPayload = JSON.parse(testPayloadStr);
      } catch (jsonErr) {
        alert('Invalid JSON format in payload text!');
        setPublishing(false);
        return;
      }

      await kafkaService.publishEvent(testTopic, testEventType, parsedPayload);
      setPublishSuccess(`Event successfully published to topic '${testTopic}'!`);
      fetchKafkaData();
      setTimeout(() => setPublishSuccess(''), 4000);
    } catch (err) {
      alert('Error publishing event: ' + err.message);
    } finally {
      setPublishing(false);
    }
  };

  return (
    <div className="space-y-6 pb-12">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-6 rounded-3xl bg-gradient-to-r from-slate-900 via-sky-950/40 to-slate-900 border border-sky-500/20 shadow-xl">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="p-1.5 rounded-lg bg-sky-500/20 text-sky-400 border border-sky-500/30">
              <Radio className="w-5 h-5 animate-pulse" />
            </span>
            <h1 className="text-xl font-bold text-white tracking-tight">Apache Kafka Event Stream</h1>
            <span className="px-2.5 py-0.5 text-xs font-bold rounded-full bg-sky-500/20 text-sky-300 border border-sky-500/30">
              Event-Driven HMS
            </span>
          </div>
          <p className="text-xs text-slate-400">
            Real-time vitals telemetry, emergency triage alert dispatching, and asynchronous ML diagnostic streaming.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={() => setAutoRefresh(!autoRefresh)}
            className={`px-3 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-2 transition-all ${
              autoRefresh
                ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                : 'bg-slate-800 text-slate-400 border border-slate-700'
            }`}
          >
            <RefreshCw className={`w-3.5 h-3.5 ${autoRefresh ? 'animate-spin' : ''}`} />
            {autoRefresh ? 'Live Refresh (3s)' : 'Paused'}
          </button>
          <button
            onClick={fetchKafkaData}
            className="px-4 py-1.5 rounded-xl bg-sky-600 hover:bg-sky-500 text-white text-xs font-bold transition-all shadow-md shadow-sky-600/30 flex items-center gap-1.5"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            Fetch Now
          </button>
        </div>
      </div>

      {/* Cluster Status Metrics Bar */}
      {kafkaStatus && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 flex items-center gap-3.5">
            <div className="p-3 rounded-xl bg-sky-500/10 text-sky-400 border border-sky-500/20">
              <Server className="w-5 h-5" />
            </div>
            <div>
              <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Cluster Connection</p>
              <div className="flex items-center gap-1.5 mt-0.5">
                <span className={`w-2 h-2 rounded-full ${kafkaStatus.is_connected ? 'bg-emerald-400 animate-ping' : 'bg-amber-400'}`} />
                <p className="text-xs font-bold text-white truncate max-w-[140px]">{kafkaStatus.mode}</p>
              </div>
            </div>
          </div>

          <div className="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 flex items-center gap-3.5">
            <div className="p-3 rounded-xl bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
              <Zap className="w-5 h-5" />
            </div>
            <div>
              <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Total Events Streamed</p>
              <p className="text-lg font-black text-white">{kafkaStatus.total_events_published}</p>
            </div>
          </div>

          <div className="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 flex items-center gap-3.5">
            <div className="p-3 rounded-xl bg-rose-500/10 text-rose-400 border border-rose-500/20">
              <AlertTriangle className="w-5 h-5" />
            </div>
            <div>
              <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Emergency Alerts</p>
              <p className="text-lg font-black text-rose-400">{kafkaStatus.emergency_alerts_triggered}</p>
            </div>
          </div>

          <div className="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 flex items-center gap-3.5">
            <div className="p-3 rounded-xl bg-teal-500/10 text-teal-400 border border-teal-500/20">
              <Layers className="w-5 h-5" />
            </div>
            <div>
              <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Active Kafka Topics</p>
              <p className="text-lg font-black text-white">{kafkaStatus.topics ? kafkaStatus.topics.length : 6}</p>
            </div>
          </div>
        </div>
      )}

      {/* Topics Overview Cards */}
      <div>
        <h2 className="text-sm font-bold text-slate-300 uppercase tracking-wider mb-3 flex items-center gap-2">
          <Database className="w-4 h-4 text-sky-400" />
          Kafka Managed Event Topics
        </h2>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3.5">
          {kafkaStatus?.topics?.map((top) => {
            const isSelected = selectedTopic === top.topic_name;
            return (
              <div
                key={top.name}
                onClick={() => setSelectedTopic(isSelected ? '' : top.topic_name)}
                className={`p-4 rounded-2xl cursor-pointer transition-all duration-200 border ${
                  isSelected
                    ? 'bg-sky-950/60 border-sky-500 shadow-lg shadow-sky-500/10'
                    : 'bg-slate-900/80 border-slate-800 hover:border-slate-700 hover:bg-slate-800/50'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-extrabold uppercase px-2 py-0.5 rounded-md bg-slate-800 text-sky-400 border border-slate-700">
                    {top.name}
                  </span>
                  <span className="text-xs font-bold text-slate-400">
                    {top.message_count} {top.message_count === 1 ? 'msg' : 'msgs'}
                  </span>
                </div>
                <p className="text-xs font-mono font-bold text-slate-200 mt-2 truncate">{top.topic_name}</p>
              </div>
            );
          })}
        </div>
      </div>

      {/* Grid: Terminal Stream + Publisher Tool */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Stream Terminal Log */}
        <div className="lg:col-span-2 space-y-3">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-bold text-slate-300 uppercase tracking-wider flex items-center gap-2">
              <Terminal className="w-4 h-4 text-emerald-400" />
              Live Topic Event Terminal Stream
            </h2>
            {selectedTopic && (
              <button
                onClick={() => setSelectedTopic('')}
                className="text-[11px] font-semibold text-sky-400 hover:underline"
              >
                Clear Filter ({selectedTopic})
              </button>
            )}
          </div>

          <div className="p-4 rounded-2xl bg-slate-950 border border-slate-800/80 shadow-2xl font-mono text-xs overflow-hidden">
            <div className="flex items-center justify-between pb-3 border-b border-slate-800 text-slate-500 text-[11px]">
              <span>Topic: {selectedTopic || 'ALL_TOPICS'}</span>
              <span>Buffer: {events.length} events</span>
            </div>

            <div className="mt-3 space-y-3 max-h-[460px] overflow-y-auto pr-2 custom-scrollbar">
              {events.length === 0 ? (
                <div className="text-center py-12 text-slate-600 font-sans">
                  <Activity className="w-8 h-8 mx-auto mb-2 opacity-40 animate-pulse" />
                  <p className="text-xs font-semibold">No Kafka stream events captured in current topic filter.</p>
                  <p className="text-[11px] mt-1 text-slate-500">Record patient vitals or trigger a test event to see live data.</p>
                </div>
              ) : (
                events.map((evt, idx) => (
                  <div
                    key={evt.event_id || idx}
                    className="p-3 rounded-xl bg-slate-900/90 border border-slate-800/90 hover:border-sky-500/40 transition-colors"
                  >
                    <div className="flex items-center justify-between mb-1.5">
                      <div className="flex items-center gap-2">
                        <span className="w-2 h-2 rounded-full bg-emerald-400" />
                        <span className="font-bold text-sky-300">{evt.event_type}</span>
                        <span className="text-[10px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-400">
                          {evt.topic}
                        </span>
                      </div>
                      <span className="text-[10px] text-slate-500">{evt.timestamp}</span>
                    </div>

                    <pre className="p-2.5 rounded-lg bg-slate-950 text-slate-300 text-[11px] overflow-x-auto border border-slate-900">
                      {JSON.stringify(evt.payload, null, 2)}
                    </pre>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>

        {/* Manual Test Producer Tool */}
        <div className="space-y-3">
          <h2 className="text-sm font-bold text-slate-300 uppercase tracking-wider flex items-center gap-2">
            <Send className="w-4 h-4 text-sky-400" />
            Publish Test Event
          </h2>

          <div className="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 space-y-4">
            {publishSuccess && (
              <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
                <span>{publishSuccess}</span>
              </div>
            )}

            <form onSubmit={handlePublishTestEvent} className="space-y-3">
              <div>
                <label className="block text-[11px] font-bold text-slate-400 mb-1">Target Topic</label>
                <select
                  value={testTopic}
                  onChange={(e) => setTestTopic(e.target.value)}
                  className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-sky-500"
                >
                  <option value="kaire-vitals-stream">kaire-vitals-stream</option>
                  <option value="kaire-emergency-alerts">kaire-emergency-alerts</option>
                  <option value="kaire-ml-predictions">kaire-ml-predictions</option>
                  <option value="kaire-appointments">kaire-appointments</option>
                  <option value="kaire-notifications">kaire-notifications</option>
                  <option value="kaire-audit-logs">kaire-audit-logs</option>
                </select>
              </div>

              <div>
                <label className="block text-[11px] font-bold text-slate-400 mb-1">Event Type Header</label>
                <input
                  type="text"
                  value={testEventType}
                  onChange={(e) => setTestEventType(e.target.value)}
                  className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-sky-500"
                  placeholder="e.g. VITAL_RECORDED"
                />
              </div>

              <div>
                <label className="block text-[11px] font-bold text-slate-400 mb-1">JSON Payload Body</label>
                <textarea
                  rows={8}
                  value={testPayloadStr}
                  onChange={(e) => setTestPayloadStr(e.target.value)}
                  className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 font-mono text-[11px] text-sky-200 focus:outline-none focus:border-sky-500"
                />
              </div>

              <button
                type="submit"
                disabled={publishing}
                className="w-full py-2.5 rounded-xl bg-gradient-to-r from-sky-600 to-sky-500 hover:from-sky-500 hover:to-sky-400 text-white font-bold text-xs shadow-lg shadow-sky-500/20 transition-all flex items-center justify-center gap-2"
              >
                {publishing ? (
                  <>
                    <RefreshCw className="w-4 h-4 animate-spin" />
                    Publishing Event...
                  </>
                ) : (
                  <>
                    <Play className="w-4 h-4 fill-current" />
                    Stream to Kafka Broker
                  </>
                )}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};
