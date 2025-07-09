#!/usr/bin/env python3
"""
tracer_router_widget.py - GUI Widget for DAWN Tracer Router System
Provides interactive visualization and control for cognitive tracer routing and genealogy integration.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
from datetime import datetime
from typing import Dict, List, Optional, Any

# Import our systems
try:
    from tracer_router import TracerRouter, TracerType, RouteResult
    from integration.tracer_rebloom_integration import TracerRebloomIntegration
except ImportError:
    print("Warning: Could not import tracer systems. Running in demo mode.")
    TracerRouter = None
    TracerRebloomIntegration = None


class TracerRouterWidget:
    """
    Interactive GUI widget for DAWN tracer routing system with comprehensive
    visualization and control capabilities.
    """
    
    def __init__(self, parent=None):
        """Initialize the tracer router widget"""
        self.parent = parent if parent else tk.Tk()
        
        # Initialize systems
        if TracerRouter and TracerRebloomIntegration:
            self.integration = TracerRebloomIntegration()
            self.tracer_router = self.integration.tracer_router
            self.rebloom_tracker = self.integration.rebloom_tracker
        else:
            self.integration = None
            self.tracer_router = None
            self.rebloom_tracker = None
        
        # Widget state
        self.auto_refresh = False
        self.refresh_interval = 3.0  # seconds
        self.last_route_results = []
        
        # Initialize GUI
        self.setup_gui()
        self.setup_demo_data()
        
        # Start auto-refresh if enabled
        if self.auto_refresh:
            self.start_auto_refresh()
        
        print("[TracerRouterWidget] 🕸️ GUI widget initialized")
    
    def setup_gui(self):
        """Setup the GUI components"""
        if isinstance(self.parent, tk.Tk):
            self.parent.title("DAWN Tracer Router System")
            self.parent.geometry("1000x700")
        
        # Create main container
        self.main_frame = ttk.Frame(self.parent)
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # Create tabs
        self.create_routing_tab()
        self.create_family_analysis_tab()
        self.create_performance_tab()
        self.create_predictions_tab()
        
        # Create status bar
        self.create_status_bar()
    
    def create_routing_tab(self):
        """Create the tracer routing tab"""
        self.routing_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.routing_frame, text="🕸️ Tracer Routing")
        
        # Control panel
        control_frame = ttk.LabelFrame(self.routing_frame, text="Routing Controls", padding=10)
        control_frame.pack(fill='x', padx=5, pady=5)
        
        # Tracer selection
        ttk.Label(control_frame, text="Tracer Type:").grid(row=0, column=0, sticky='w', padx=(0, 10))
        self.tracer_var = tk.StringVar(value="owl")
        tracer_combo = ttk.Combobox(control_frame, textvariable=self.tracer_var, 
                                   values=["owl", "crow", "spider", "whale"], state="readonly", width=15)
        tracer_combo.grid(row=0, column=1, sticky='w', padx=(0, 20))
        
        # Target bloom selection
        ttk.Label(control_frame, text="Target Bloom:").grid(row=0, column=2, sticky='w', padx=(0, 10))
        self.target_var = tk.StringVar(value="bloom_001")
        self.target_entry = ttk.Entry(control_frame, textvariable=self.target_var, width=15)
        self.target_entry.grid(row=0, column=3, sticky='w', padx=(0, 20))
        
        # Route button
        route_btn = ttk.Button(control_frame, text="🎯 Route Tracer", command=self.route_tracer)
        route_btn.grid(row=0, column=4, sticky='w', padx=(0, 10))
        
        # Get available routes button
        available_btn = ttk.Button(control_frame, text="📋 Get Available Routes", command=self.get_available_routes)
        available_btn.grid(row=0, column=5, sticky='w')
        
        # Results display
        results_frame = ttk.LabelFrame(self.routing_frame, text="Routing Results", padding=10)
        results_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Route result display
        self.route_result_text = scrolledtext.ScrolledText(results_frame, height=15, wrap='word')
        self.route_result_text.pack(fill='both', expand=True)
        
        # Available routes tree
        routes_frame = ttk.LabelFrame(self.routing_frame, text="Available Routes", padding=10)
        routes_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create treeview for available routes
        columns = ('bloom_id', 'score', 'time', 'probability', 'reason')
        self.routes_tree = ttk.Treeview(routes_frame, columns=columns, show='headings', height=8)
        
        # Configure columns
        self.routes_tree.heading('bloom_id', text='Bloom ID')
        self.routes_tree.heading('score', text='Score')
        self.routes_tree.heading('time', text='Est. Time')
        self.routes_tree.heading('probability', text='Probability')
        self.routes_tree.heading('reason', text='Routing Reason')
        
        self.routes_tree.column('bloom_id', width=100)
        self.routes_tree.column('score', width=80)
        self.routes_tree.column('time', width=80)
        self.routes_tree.column('probability', width=80)
        self.routes_tree.column('reason', width=300)
        
        # Add scrollbar for routes tree
        routes_scrollbar = ttk.Scrollbar(routes_frame, orient='vertical', command=self.routes_tree.yview)
        self.routes_tree.configure(yscrollcommand=routes_scrollbar.set)
        
        self.routes_tree.pack(side='left', fill='both', expand=True)
        routes_scrollbar.pack(side='right', fill='y')
    
    def create_family_analysis_tab(self):
        """Create the family analysis tab"""
        self.family_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.family_frame, text="🧬 Family Analysis")
        
        # Family controls
        family_control_frame = ttk.LabelFrame(self.family_frame, text="Family Analysis Controls", padding=10)
        family_control_frame.pack(fill='x', padx=5, pady=5)
        
        # Root bloom selection
        ttk.Label(family_control_frame, text="Root Bloom:").grid(row=0, column=0, sticky='w', padx=(0, 10))
        self.family_root_var = tk.StringVar(value="bloom_001")
        self.family_root_entry = ttk.Entry(family_control_frame, textvariable=self.family_root_var, width=15)
        self.family_root_entry.grid(row=0, column=1, sticky='w', padx=(0, 20))
        
        # Analyze family button
        analyze_family_btn = ttk.Button(family_control_frame, text="🔍 Analyze Family", command=self.analyze_family)
        analyze_family_btn.grid(row=0, column=2, sticky='w', padx=(0, 10))
        
        # Get family suggestions button
        suggest_btn = ttk.Button(family_control_frame, text="💡 Get Tracer Suggestions", command=self.get_family_suggestions)
        suggest_btn.grid(row=0, column=3, sticky='w', padx=(0, 10))
        
        # Route to family cluster button
        cluster_btn = ttk.Button(family_control_frame, text="🕸️ Route to Cluster", command=self.route_to_family_cluster)
        cluster_btn.grid(row=0, column=4, sticky='w')
        
        # Family results display
        family_results_frame = ttk.LabelFrame(self.family_frame, text="Family Analysis Results", padding=10)
        family_results_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.family_results_text = scrolledtext.ScrolledText(family_results_frame, height=20, wrap='word')
        self.family_results_text.pack(fill='both', expand=True)
    
    def create_performance_tab(self):
        """Create the performance monitoring tab"""
        self.performance_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.performance_frame, text="📊 Performance")
        
        # Performance controls
        perf_control_frame = ttk.LabelFrame(self.performance_frame, text="Performance Controls", padding=10)
        perf_control_frame.pack(fill='x', padx=5, pady=5)
        
        # Refresh button
        refresh_btn = ttk.Button(perf_control_frame, text="🔄 Refresh Stats", command=self.refresh_performance)
        refresh_btn.pack(side='left', padx=(0, 10))
        
        # Auto-refresh toggle
        self.auto_refresh_var = tk.BooleanVar(value=self.auto_refresh)
        auto_refresh_check = ttk.Checkbutton(perf_control_frame, text="Auto-refresh (3s)", 
                                           variable=self.auto_refresh_var, command=self.toggle_auto_refresh)
        auto_refresh_check.pack(side='left', padx=(0, 10))
        
        # Clear stats button
        clear_btn = ttk.Button(perf_control_frame, text="🧹 Clear Stats", command=self.clear_stats)
        clear_btn.pack(side='left', padx=(0, 10))
        
        # Export data button
        export_btn = ttk.Button(perf_control_frame, text="📁 Export Data", command=self.export_data)
        export_btn.pack(side='left')
        
        # Statistics display
        stats_frame = ttk.LabelFrame(self.performance_frame, text="System Statistics", padding=10)
        stats_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.stats_text = scrolledtext.ScrolledText(stats_frame, height=25, wrap='word')
        self.stats_text.pack(fill='both', expand=True)
    
    def create_predictions_tab(self):
        """Create the predictions tab"""
        self.predictions_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.predictions_frame, text="🔮 Predictions")
        
        # Prediction controls
        pred_control_frame = ttk.LabelFrame(self.predictions_frame, text="Prediction Controls", padding=10)
        pred_control_frame.pack(fill='x', padx=5, pady=5)
        
        # Tracer type for predictions
        ttk.Label(pred_control_frame, text="Tracer Type:").grid(row=0, column=0, sticky='w', padx=(0, 10))
        self.pred_tracer_var = tk.StringVar(value="owl")
        pred_tracer_combo = ttk.Combobox(pred_control_frame, textvariable=self.pred_tracer_var, 
                                        values=["owl", "crow", "spider", "whale"], state="readonly", width=15)
        pred_tracer_combo.grid(row=0, column=1, sticky='w', padx=(0, 20))
        
        # Minimum score threshold
        ttk.Label(pred_control_frame, text="Min Score:").grid(row=0, column=2, sticky='w', padx=(0, 10))
        self.min_score_var = tk.DoubleVar(value=0.6)
        min_score_spin = ttk.Spinbox(pred_control_frame, textvariable=self.min_score_var, 
                                    from_=0.0, to=1.0, increment=0.1, width=10)
        min_score_spin.grid(row=0, column=3, sticky='w', padx=(0, 20))
        
        # Predict button
        predict_btn = ttk.Button(pred_control_frame, text="🔮 Predict Optimal Targets", command=self.predict_rebloom_targets)
        predict_btn.grid(row=0, column=4, sticky='w')
        
        # Predictions display
        pred_results_frame = ttk.LabelFrame(self.predictions_frame, text="Rebloom Predictions", padding=10)
        pred_results_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.predictions_text = scrolledtext.ScrolledText(pred_results_frame, height=20, wrap='word')
        self.predictions_text.pack(fill='both', expand=True)
    
    def create_status_bar(self):
        """Create status bar"""
        self.status_frame = ttk.Frame(self.main_frame)
        self.status_frame.pack(fill='x', pady=(5, 0))
        
        self.status_label = ttk.Label(self.status_frame, text="Ready", relief='sunken')
        self.status_label.pack(side='left', fill='x', expand=True)
        
        # System status indicators
        self.router_status = ttk.Label(self.status_frame, text="Router: ✅", relief='sunken')
        self.router_status.pack(side='right', padx=(5, 0))
        
        self.tracker_status = ttk.Label(self.status_frame, text="Tracker: ✅", relief='sunken')
        self.tracker_status.pack(side='right', padx=(5, 0))
    
    def setup_demo_data(self):
        """Setup demo data for testing"""
        if not self.tracer_router:
            return
        
        # Add demo bloom targets
        demo_blooms = [
            ('bloom_001', 0, 0.5, 0.6, {'schema': 0.6, 'coherence': 0.8, 'utility': 0.7, 'pressure': 0.3}),
            ('bloom_002', 1, 0.6, 0.7, {'schema': 0.5, 'coherence': 0.9, 'utility': 0.6, 'pressure': 0.4}),
            ('bloom_003', 1, 0.4, 0.5, {'schema': 0.7, 'coherence': 0.7, 'utility': 0.8, 'pressure': 0.2}),
            ('bloom_004', 2, 0.7, 0.8, {'schema': 0.8, 'coherence': 0.6, 'utility': 0.9, 'pressure': 0.5}),
            ('bloom_005', 2, 0.3, 0.4, {'schema': 0.4, 'coherence': 0.8, 'utility': 0.5, 'pressure': 0.6}),
            ('bloom_006', 3, 0.8, 0.9, {'schema': 0.9, 'coherence': 0.5, 'utility': 0.7, 'pressure': 0.7}),
        ]
        
        for bloom_id, depth, entropy, complexity, scup_values in demo_blooms:
            self.tracer_router.add_bloom_target(
                bloom_id=bloom_id,
                depth=depth,
                entropy=entropy,
                complexity=complexity,
                scup_values=scup_values,
                rebloom_status='stable'
            )
        
        # Add demo rebloom data
        rebloom_data = [
            ('bloom_001', None, 0.5),
            ('bloom_002', 'bloom_001', 0.6),
            ('bloom_003', 'bloom_001', 0.4),
            ('bloom_004', 'bloom_002', 0.7),
            ('bloom_005', 'bloom_002', 0.3),
            ('bloom_006', 'bloom_004', 0.8),
        ]
        
        for bloom_id, parent_id, entropy_change in rebloom_data:
            self.rebloom_tracker.log_rebloom(bloom_id, parent_id, entropy_change)
        
        self.update_status("Demo data loaded successfully")
    
    def route_tracer(self):
        """Route selected tracer to target bloom"""
        if not self.tracer_router:
            messagebox.showwarning("Warning", "Tracer router not available in demo mode")
            return
        
        tracer_type = self.tracer_var.get()
        target_bloom = self.target_var.get().strip()
        
        if not target_bloom:
            messagebox.showerror("Error", "Please enter a target bloom ID")
            return
        
        self.update_status(f"Routing {tracer_type} to {target_bloom}...")
        
        # Route the tracer
        route_result = self.tracer_router.route(tracer_type, target_bloom)
        
        if route_result:
            # Display results
            result_text = f"🕸️ TRACER ROUTING RESULT\n"
            result_text += f"{'=' * 50}\n\n"
            result_text += f"✅ Successfully routed {tracer_type.upper()} to {target_bloom}\n\n"
            result_text += f"📊 ROUTING METRICS:\n"
            result_text += f"  • Route Score: {route_result.route_score:.3f}\n"
            result_text += f"  • Estimated Time: {route_result.estimated_time:.1f} seconds\n"
            result_text += f"  • Resource Cost: {route_result.resource_cost:.3f}\n"
            result_text += f"  • Success Probability: {route_result.success_probability:.1%}\n\n"
            result_text += f"🛤️ COGNITIVE PATHWAY:\n"
            result_text += f"  {' → '.join(route_result.route_path)}\n\n"
            result_text += f"💭 ROUTING REASON:\n"
            result_text += f"  {route_result.routing_reason}\n\n"
            result_text += f"🕐 Timestamp: {route_result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"
            
            self.route_result_text.delete(1.0, tk.END)
            self.route_result_text.insert(1.0, result_text)
            
            self.update_status(f"Successfully routed {tracer_type} to {target_bloom}")
        else:
            error_text = f"❌ ROUTING FAILED\n"
            error_text += f"{'=' * 50}\n\n"
            error_text += f"Failed to route {tracer_type.upper()} to {target_bloom}\n"
            error_text += f"Possible reasons:\n"
            error_text += f"  • Target bloom not found\n"
            error_text += f"  • Route score too low (<30%)\n"
            error_text += f"  • Invalid tracer type\n"
            
            self.route_result_text.delete(1.0, tk.END)
            self.route_result_text.insert(1.0, error_text)
            
            self.update_status(f"Failed to route {tracer_type} to {target_bloom}")
    
    def get_available_routes(self):
        """Get and display available routes for selected tracer"""
        if not self.tracer_router:
            messagebox.showwarning("Warning", "Tracer router not available in demo mode")
            return
        
        tracer_type = self.tracer_var.get()
        
        self.update_status(f"Getting available routes for {tracer_type}...")
        
        # Get available routes
        available_routes = self.tracer_router.get_available_routes(tracer_type, limit=15)
        
        # Clear existing items
        for item in self.routes_tree.get_children():
            self.routes_tree.delete(item)
        
        # Populate tree with available routes
        for route in available_routes:
            self.routes_tree.insert('', 'end', values=(
                route['bloom_id'],
                f"{route['route_score']:.3f}",
                f"{route['estimated_time']:.1f}s",
                f"{route['success_probability']:.1%}",
                route['routing_reason'][:50] + "..." if len(route['routing_reason']) > 50 else route['routing_reason']
            ))
        
        self.update_status(f"Found {len(available_routes)} available routes for {tracer_type}")
    
    def analyze_family(self):
        """Analyze family structure and display integrated analysis"""
        if not self.integration:
            messagebox.showwarning("Warning", "Integration system not available in demo mode")
            return
        
        root_bloom = self.family_root_var.get().strip()
        tracer_type = self.tracer_var.get()
        
        if not root_bloom:
            messagebox.showerror("Error", "Please enter a root bloom ID")
            return
        
        self.update_status(f"Analyzing family of {root_bloom} with {tracer_type}...")
        
        # Perform integrated analysis
        result = self.integration.analyze_with_routing(tracer_type, root_bloom, include_family_analysis=True)
        
        if result:
            # Display comprehensive analysis
            analysis_text = f"🧬 INTEGRATED FAMILY ANALYSIS\n"
            analysis_text += f"{'=' * 60}\n\n"
            
            # Route information
            analysis_text += f"🕸️ TRACER ROUTING:\n"
            analysis_text += f"  • Tracer: {result.tracer_route.tracer_type.upper()}\n"
            analysis_text += f"  • Target: {result.tracer_route.target_bloom_id}\n"
            analysis_text += f"  • Route Score: {result.tracer_route.route_score:.3f}\n"
            analysis_text += f"  • Path: {' → '.join(result.tracer_route.route_path)}\n\n"
            
            # Genealogy information
            analysis_text += f"🧬 GENEALOGY ANALYSIS:\n"
            genealogy = result.genealogy_analysis
            analysis_text += f"  • Has Genealogy Data: {genealogy.get('has_genealogy_data', False)}\n"
            analysis_text += f"  • Depth: {genealogy.get('depth', 0)}\n"
            
            if 'family_statistics' in genealogy:
                fstats = genealogy['family_statistics']
                analysis_text += f"  • Total Family Size: {fstats.get('total_family_size', 0)}\n"
                analysis_text += f"  • Generation Depth: {fstats.get('generation_depth', 0)}\n"
                analysis_text += f"  • Descendant Count: {fstats.get('descendant_count', 0)}\n"
                analysis_text += f"  • Is Root: {fstats.get('is_root', False)}\n"
                analysis_text += f"  • Is Leaf: {fstats.get('is_leaf', False)}\n"
            
            analysis_text += "\n"
            
            # Family context
            analysis_text += f"🏠 FAMILY CONTEXT:\n"
            context = result.family_context
            analysis_text += f"  • Context Type: {context.get('context_type', 'unknown')}\n"
            analysis_text += f"  • Match Score: {context.get('context_match_score', 0.0):.3f}\n"
            analysis_text += f"  • Family Size: {context.get('family_size', 0)}\n"
            analysis_text += f"  • Generation Depth: {context.get('generation_depth', 0)}\n\n"
            
            # Cognitive insights
            analysis_text += f"💡 COGNITIVE INSIGHTS:\n"
            for i, insight in enumerate(result.cognitive_insights, 1):
                analysis_text += f"  {i}. {insight}\n"
            analysis_text += "\n"
            
            # Routing recommendations
            analysis_text += f"🎯 ROUTING RECOMMENDATIONS:\n"
            for i, rec in enumerate(result.routing_recommendations, 1):
                analysis_text += f"  {i}. {rec}\n"
            
            analysis_text += f"\n🕐 Analysis completed at: {result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"
            
            self.family_results_text.delete(1.0, tk.END)
            self.family_results_text.insert(1.0, analysis_text)
            
            self.update_status(f"Family analysis complete for {root_bloom}")
        else:
            error_text = f"❌ FAMILY ANALYSIS FAILED\n"
            error_text += f"{'=' * 50}\n\n"
            error_text += f"Failed to analyze family of {root_bloom}\n"
            error_text += f"Check that the bloom exists and has valid routing targets.\n"
            
            self.family_results_text.delete(1.0, tk.END)
            self.family_results_text.insert(1.0, error_text)
            
            self.update_status(f"Failed to analyze family of {root_bloom}")
    
    def get_family_suggestions(self):
        """Get tracer suggestions for family analysis"""
        if not self.integration:
            messagebox.showwarning("Warning", "Integration system not available in demo mode")
            return
        
        root_bloom = self.family_root_var.get().strip()
        
        if not root_bloom:
            messagebox.showerror("Error", "Please enter a root bloom ID")
            return
        
        self.update_status(f"Getting tracer suggestions for family of {root_bloom}...")
        
        # Get suggestions
        suggestions = self.integration.suggest_optimal_tracers_for_family(root_bloom, max_suggestions=4)
        
        if suggestions:
            suggestion_text = f"💡 TRACER SUGGESTIONS FOR FAMILY\n"
            suggestion_text += f"{'=' * 50}\n\n"
            suggestion_text += f"Root Bloom: {root_bloom}\n\n"
            
            for i, suggestion in enumerate(suggestions, 1):
                emoji = {'owl': '🦉', 'crow': '🐦‍⬛', 'spider': '🕷️', 'whale': '🐋'}.get(suggestion['tracer_type'], '🔍')
                suggestion_text += f"{i}. {emoji} {suggestion['tracer_type'].upper()}\n"
                suggestion_text += f"   • Match Score: {suggestion['family_match_score']:.3f}\n"
                suggestion_text += f"   • Family Depth: {suggestion['family_depth']}\n"
                suggestion_text += f"   • Family Size: {suggestion['family_size']}\n"
                suggestion_text += f"   • Coverage: {suggestion['estimated_coverage']:.1%}\n"
                suggestion_text += f"   • Reason: {suggestion['suggestion_reason']}\n\n"
            
            self.family_results_text.delete(1.0, tk.END)
            self.family_results_text.insert(1.0, suggestion_text)
            
            self.update_status(f"Generated {len(suggestions)} tracer suggestions")
        else:
            self.family_results_text.delete(1.0, tk.END)
            self.family_results_text.insert(1.0, "No tracer suggestions available for this family.")
            self.update_status("No suggestions available")
    
    def route_to_family_cluster(self):
        """Route tracer to entire family cluster"""
        if not self.integration:
            messagebox.showwarning("Warning", "Integration system not available in demo mode")
            return
        
        root_bloom = self.family_root_var.get().strip()
        tracer_type = self.tracer_var.get()
        
        if not root_bloom:
            messagebox.showerror("Error", "Please enter a root bloom ID")
            return
        
        self.update_status(f"Routing {tracer_type} to family cluster of {root_bloom}...")
        
        # Route to family cluster
        route_results = self.integration.route_tracer_to_family_cluster(tracer_type, root_bloom)
        
        if route_results:
            cluster_text = f"🕸️ FAMILY CLUSTER ROUTING RESULTS\n"
            cluster_text += f"{'=' * 60}\n\n"
            cluster_text += f"Tracer: {tracer_type.upper()}\n"
            cluster_text += f"Root Bloom: {root_bloom}\n"
            cluster_text += f"Successfully routed to {len(route_results)} family members\n\n"
            
            for i, result in enumerate(route_results, 1):
                cluster_text += f"{i}. Target: {result.target_bloom_id}\n"
                cluster_text += f"   • Score: {result.route_score:.3f}\n"
                cluster_text += f"   • Time: {result.estimated_time:.1f}s\n"
                cluster_text += f"   • Path: {' → '.join(result.route_path[-3:])}\n"
                cluster_text += f"   • Reason: {result.routing_reason[:60]}...\n\n"
            
            self.family_results_text.delete(1.0, tk.END)
            self.family_results_text.insert(1.0, cluster_text)
            
            self.update_status(f"Routed to {len(route_results)} family members")
        else:
            self.family_results_text.delete(1.0, tk.END)
            self.family_results_text.insert(1.0, "No family cluster routes available.")
            self.update_status("No cluster routes available")
    
    def predict_rebloom_targets(self):
        """Predict optimal rebloom targets"""
        if not self.integration:
            messagebox.showwarning("Warning", "Integration system not available in demo mode")
            return
        
        tracer_type = self.pred_tracer_var.get()
        min_score = self.min_score_var.get()
        
        self.update_status(f"Predicting optimal rebloom targets for {tracer_type}...")
        
        # Get predictions
        predictions = self.integration.predict_optimal_rebloom_targets(tracer_type, min_score=min_score)
        
        if predictions:
            pred_text = f"🔮 REBLOOM TARGET PREDICTIONS\n"
            pred_text += f"{'=' * 50}\n\n"
            pred_text += f"Tracer: {tracer_type.upper()}\n"
            pred_text += f"Minimum Score: {min_score:.1f}\n"
            pred_text += f"Found {len(predictions)} optimal targets\n\n"
            
            for i, pred in enumerate(predictions, 1):
                pred_text += f"{i}. Target: {pred['target_bloom_id']}\n"
                pred_text += f"   • Optimization Score: {pred['optimization_score']:.3f}\n"
                pred_text += f"   • Route Score: {pred['route_score']:.3f}\n"
                pred_text += f"   • Genealogy Depth: {pred['genealogy_depth']}\n"
                pred_text += f"   • Family Size: {pred['family_size']}\n"
                pred_text += f"   • Estimated Impact: {pred['estimated_impact']:.1%}\n"
                pred_text += f"   • Reason: {pred['prediction_reason']}\n\n"
            
            self.predictions_text.delete(1.0, tk.END)
            self.predictions_text.insert(1.0, pred_text)
            
            self.update_status(f"Found {len(predictions)} optimal rebloom targets")
        else:
            self.predictions_text.delete(1.0, tk.END)
            self.predictions_text.insert(1.0, f"No optimal rebloom targets found with minimum score {min_score:.1f}")
            self.update_status("No optimal targets found")
    
    def refresh_performance(self):
        """Refresh and display performance statistics"""
        if not self.integration:
            messagebox.showwarning("Warning", "Integration system not available in demo mode")
            return
        
        self.update_status("Refreshing performance statistics...")
        
        # Get comprehensive statistics
        stats = self.integration.get_integration_statistics()
        router_stats = stats.get('tracer_router_stats', {})
        tracker_stats = stats.get('rebloom_tracker_stats', {})
        
        # Format statistics display
        stats_text = f"📊 DAWN TRACER ROUTER PERFORMANCE\n"
        stats_text += f"{'=' * 60}\n\n"
        
        # Integration statistics
        stats_text += f"🧠 INTEGRATION STATISTICS:\n"
        stats_text += f"  • Total Analyses: {stats.get('total_analyses', 0)}\n"
        stats_text += f"  • Successful Integrations: {stats.get('successful_integrations', 0)}\n"
        stats_text += f"  • Integration Efficiency: {stats.get('integration_efficiency', 0.0):.1%}\n"
        stats_text += f"  • Cache Hits: {stats.get('cache_hits', 0)}\n"
        stats_text += f"  • Tracer-Genealogy Matches: {stats.get('tracer_genealogy_matches', 0)}\n\n"
        
        # Router statistics
        stats_text += f"🕸️ TRACER ROUTER STATISTICS:\n"
        stats_text += f"  • Total Routes: {router_stats.get('total_routes', 0)}\n"
        stats_text += f"  • Successful Routes: {router_stats.get('successful_routes', 0)}\n"
        stats_text += f"  • Success Rate: {router_stats.get('success_rate', 0.0):.1%}\n"
        stats_text += f"  • Average Routing Time: {router_stats.get('average_routing_time', 0.0):.3f}s\n"
        stats_text += f"  • Active Routes: {router_stats.get('active_routes', 0)}\n"
        stats_text += f"  • Cached Routes: {router_stats.get('cached_routes', 0)}\n"
        stats_text += f"  • Bloom Targets: {router_stats.get('bloom_targets', 0)}\n\n"
        
        # Tracer usage
        tracer_usage = router_stats.get('tracer_usage', {})
        if tracer_usage:
            stats_text += f"🔍 TRACER USAGE:\n"
            for tracer, count in tracer_usage.items():
                emoji = {'owl': '🦉', 'crow': '🐦‍⬛', 'spider': '🕷️', 'whale': '🐋'}.get(tracer, '🔍')
                stats_text += f"  • {emoji} {tracer.title()}: {count}\n"
            stats_text += "\n"
        
        # Rebloom tracker statistics
        stats_text += f"🧬 REBLOOM TRACKER STATISTICS:\n"
        stats_text += f"  • Total Blooms: {tracker_stats.get('total_blooms', 0)}\n"
        stats_text += f"  • Total Rebloom Events: {tracker_stats.get('total_rebloom_events', 0)}\n"
        stats_text += f"  • Maximum Depth: {tracker_stats.get('max_depth', 0)}\n"
        stats_text += f"  • Average Depth: {tracker_stats.get('average_depth', 0.0):.1f}\n"
        stats_text += f"  • Root Blooms: {tracker_stats.get('root_blooms', 0)}\n"
        stats_text += f"  • Leaf Blooms: {tracker_stats.get('leaf_blooms', 0)}\n\n"
        
        stats_text += f"🕐 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(1.0, stats_text)
        
        self.update_status("Performance statistics refreshed")
    
    def toggle_auto_refresh(self):
        """Toggle auto-refresh mode"""
        self.auto_refresh = self.auto_refresh_var.get()
        if self.auto_refresh:
            self.start_auto_refresh()
            self.update_status("Auto-refresh enabled")
        else:
            self.update_status("Auto-refresh disabled")
    
    def start_auto_refresh(self):
        """Start auto-refresh thread"""
        if self.auto_refresh:
            self.refresh_performance()
            self.parent.after(int(self.refresh_interval * 1000), self.start_auto_refresh)
    
    def clear_stats(self):
        """Clear statistics and reset counters"""
        if not self.tracer_router:
            return
        
        # Reset router statistics
        if hasattr(self.tracer_router, 'routing_stats'):
            self.tracer_router.routing_stats = {
                'total_routes': 0,
                'successful_routes': 0,
                'cache_hits': 0,
                'tracer_usage': {},
                'average_routing_time': 0.0
            }
        
        # Clear active routes
        if hasattr(self.tracer_router, 'clear_active_routes'):
            self.tracer_router.clear_active_routes()
        
        self.refresh_performance()
        self.update_status("Statistics cleared")
    
    def export_data(self):
        """Export integration data"""
        if not self.integration:
            messagebox.showwarning("Warning", "Integration system not available in demo mode")
            return
        
        try:
            filename = self.integration.export_integration_data()
            messagebox.showinfo("Export Complete", f"Data exported to: {filename}")
            self.update_status(f"Data exported to {filename}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export data: {str(e)}")
            self.update_status("Export failed")
    
    def update_status(self, message: str):
        """Update status bar message"""
        self.status_label.config(text=message)
        self.parent.update_idletasks()
    
    def run(self):
        """Run the widget (for standalone use)"""
        if isinstance(self.parent, tk.Tk):
            self.parent.mainloop()


# Example usage and testing
if __name__ == "__main__":
    print("🕸️ DAWN Tracer Router Widget Demo")
    print("=" * 50)
    
    # Create and run the widget
    widget = TracerRouterWidget()
    widget.run() 