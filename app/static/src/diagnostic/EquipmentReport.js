import React from 'react';
import ReactDOM from 'react-dom';
import * as d3 from "d3";
import EquipmentForm from './EquipmentForm';

function clone(obj) {
    if (null == obj || "object" != typeof obj) return obj;
    var copy = obj.constructor();
    for (var attr in obj) {
        if (obj.hasOwnProperty(attr)) copy[attr] = obj[attr];
    }
    return copy;
}

var EquipmentReport = React.createClass({
    getInitialState: function () {
        return {
            equipmentId : 0,
            tests : [],
            tests_data : {}
        }
    },

    componentDidMount: function () { 
        var _self = this;
        var equipmentId = this.props.params['equipmentId'];
        $.get(url.info.replace(":id", equipmentId), function(data){
            _self.setState({"equipment" : data.equipment , "equipment_item" : data.equipment_item, equipmentId : equipmentId})
        }, "json");
        $.get("/api/v1.0/test_result/item_id/" + equipmentId + "/all", function(data){
            _self.setState({"tests" : data.result})
        }, "json");
        $.get(url.graph + '?id=' + equipmentId, function (data) {
            _self.setState({"tests_data" : data})
        }, 'json')
    },

    download:function(){
        
    },

    render: function () {
        var _self = this;
        if (!this.state.equipment) {
            return null
        }
        //this.props.params['equipmentId']
        var test_results = [];
        for (var test_type in this.state.tests_data){
            var obj = this.state.tests_data[test_type];
            var dates = [];
            dates.push(<th>Date</th>);
            var items = [];
            for (var k in obj[0].data){
                dates.push(<th>{obj[0].data[k].day}</th>)
            }
            for (var k in obj){
                var item_data = obj[k];
                
                var results = [];
                results.push(<td>{item_data.label}</td>);
                for (var res_key in item_data.data){
                    results.push(<td>{item_data.data[res_key].count}</td>)
                }
                items.push(<tr>
                    {results}
                </tr>)
            }
            var last_report = {};
            this.state.tests.map(function(one_test){
                if (one_test.test_type.name == test_type){
                    if (!last_report.date_analyse)
                        last_report = one_test;
                    else{
                        if (new Date(last_report.date_analyse) < new Date(one_test.date_analyse))
                            last_report = one_test;
                    }
                }
            })
            test_results.push(
                <div>    
                    <h2>{test_type}</h2>
                    <table width="100%" className="grapth_table" style={{'margin-bottom' : '10px'}}>
                        <thead>
                            <tr>
                                Last result
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Date</td>
                                <td>{last_report.date_analyse}</td>
                                <td>Analysis number</td>
                                <td>{last_report.analysis_number}</td>
                                <td>Test Reason</td>
                                <td>{last_report.test_reason.name}</td>
                            </tr>
                            <tr>
                                <td>Remark</td>
                                <td colSpan="5">{last_report.remark}</td>
                            </tr>
                        </tbody>
                    </table>
                    <table width="100%" className="grapth_table">
                        <thead>
                            <tr>
                                {dates}
                            </tr>
                        </thead>
                        <tbody>
                            {items}
                        </tbody>
                    </table>
                    <LineChart chart_data={obj}/>
                </div>
            );
        }
        return (
            <div className={"col-md-12"} >
                <h2>Equipment Report</h2>
                
                <table width="100%" className="grapth_table">
                    <thead>
                        <tr>
                            <th colSpan="6">Equipment Information</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td width="130px">Id:</td>
                            <td>{this.state.equipment.id}</td>
                            <td width="130px">Serial No:</td>
                            <td>{this.state.equipment.serial}</td>
                            <td width="130px">Name:</td>
                            <td>{this.state.equipment.equipment_number}</td>
                        </tr>
                        <tr>
                            <td >Type:</td>
                            <td>{this.state.equipment.equipment_type.name}</td>
                            <td >Description:</td>
                            <td>{this.state.equipment.description}</td>
                            <td >Comments:</td>
                            <td>{this.state.equipment.comments}</td>
                        </tr>
                        <tr>
                            <td >Location:</td>
                            <td>{this.state.equipment.location.name}</td>
                            <td >Manufacturer:</td>
                            <td>{this.state.equipment.manufacturer.name}</td>
                            <td >Year:</td>
                            <td>{this.state.equipment.manufactured}</td>
                        </tr>
                    </tbody>
                </table>
                {/*
                {this.state.tests.map(function(obj){
                    return(<div>
                        <p>{obj.date_analyse}</p>
                        <p><b>Overall Diagnostic:</b></p>
                        <p><b>Overall Recommendations: {obj.test_recommendations[0].recommendation_notes}</b></p>
                        <p><b>Comments: {obj.remark}</b></p>
                        <p><b>Analysis performed by:</b></p>
                        <hr />
                    </div>)

                })}
                */}

                {test_results}
            </div>
        );
    }
});


var Axis=React.createClass({
    propTypes: {
        h:React.PropTypes.number,
        axis:React.PropTypes.func,
        axisType:React.PropTypes.oneOf(['x','y'])

    },

    componentDidUpdate: function () { this.renderAxis(); },
    componentDidMount: function () { this.renderAxis(); },
    renderAxis: function () {
        var node = ReactDOM.findDOMNode(this);
        d3.select(node).call(this.props.axis);

    },
    render: function () {

        var translate = "translate(0,"+(this.props.h)+")";
        if (this.props.axisType == "y")
            var rect = <rect width="70" height="410" x="-70" y="-10"style={{"fill":"white"}} />;
        else
            var rect = <rect width="800" height="20" style={{"fill":"white"}} x="-20" y="1"/>
        return (
            <g transform={this.props.axisType=='x'?translate:""}>
                {rect}
                <g className="axis"  ></g>
            </g>
        );
    }

});

var Grid=React.createClass({
    propTypes: {
        h:React.PropTypes.number,
        grid:React.PropTypes.func,
        gridType:React.PropTypes.oneOf(['x','y'])
    },

    componentDidUpdate: function () { this.renderGrid(); },
    componentDidMount: function () { this.renderGrid(); },
    renderGrid: function () {
        var node = ReactDOM.findDOMNode(this);
        d3.select(node).call(this.props.grid);

    },
    render: function () {
        var translate = "translate(0,"+(this.props.h)+")";
        return (
            <g className="y-grid" transform={this.props.gridType=='x'?translate:""}>
            </g>
        );
    }

});


var LineChart=React.createClass({

    propTypes: {
        width:React.PropTypes.number,
        height:React.PropTypes.number,
        chartId:React.PropTypes.string
    },

    getDefaultProps: function() {
        return {
            width: 800,
            height: 400,
            chartId: 'v1_chart'
        };
    },
    getInitialState:function(){
        return {
            tooltip:{ display:false,data:{key:'',value:''}},
            width:this.props.width,
            margin:{top: 5, right: 50, bottom: 20, left: 0},
            chart_data:this.props.chart_data,
            scale_x:1,
            scale_y:1,
            offset_y:0,
            offset_x:0,
            mouse_pos_y:170,
            mouse_pos_x:335
        };
    },
    
    componentDidMount() {
              
    },
    
    render:function(){
        var _self = this;
        var chart_data =  clone(this.state.chart_data);
        
        var margin = {top: 25, right: 50, bottom: 20, left: 70},
            w = this.state.width - (margin.left + margin.right),
            h = this.props.height - (margin.top + margin.bottom);

        for (var k in chart_data){
            for (var item_k in chart_data[k].data){
                chart_data[k].data[item_k].date = d3.timeParse("%Y.%m.%d")(chart_data[k].data[item_k].day)
            }
        }
        var max_y = 0,
            min_y = 0,
            max_x = 0,
            min_x = 0;

        // for Y axex calculation
        max_y = d3.max(chart_data,function(d){
            return d3.max(d.data,function(dd){
                return dd.count;
            })
        });

        
        var x = d3.scaleTime()
        .domain(d3.extent(chart_data[0].data,function(d){
            return d.date;
        }))
        .rangeRound([0, w]);

        var y = d3.scaleLinear()
            .domain([min_y,max_y])
            .range([h, 0]);

        var yAxis = d3.axisLeft(y)
            .ticks(5);
            
        var xAxis = d3.axisBottom(x)
            //.tickValues(all_data.map(function(d,i){
                //return d.date;
            //}))
            //.ticks(4);

        var yGrid = d3.axisLeft(y)
            .ticks(5)
            .tickSize(-w, 0, 0)
            .tickFormat("");

        var line = d3.line()
            .x(function (d) {
                return x(d.date);
            })
            .y(function (d) {
                return y(d.count);
            }).curve(d3.curveLinear);

        var transform='translate(' + margin.left + ',' + margin.top + ')';
        
        var rows = [];
        for (var i in chart_data){
            var split_label = chart_data[i].label.split(" ");
            var className = "line shadow " + split_label[0].toLowerCase() ;
            var dot_data = clone(chart_data[i].data);
            
            var key = i + "_" + split_label[0].toLowerCase() + "_" + split_label[split_label.length - 1].toLowerCase();
            rows.push(<g key={key} ><path className={className} d={line(dot_data)} strokeLinecap="round"/></g>);
        }

        var legend = [];
        chart_data.map(function(obj){
            var className = "line " +obj.label.split(" ")[0].toLowerCase();
            legend.push(
                <div className="item">
                    <div className={className}></div>
                    <label>
                        {obj.label}
                    </label>
                </div>    
            );
        
        })
       
        return (
            <div className="row">
                <div className="col-md-8">
                    <div key="graph_div">
                        <svg id={this.props.chartId} width={this.state.width} height={this.props.height} >

                            <g transform={transform}>

                                <Grid h={h} grid={yGrid} gridType="y"/>
                                {rows}
                                
                                <g fill="white" className="graph">
                                    <Axis h={h} axis={yAxis} axisType="y" fill="white" />
                                    <Axis h={h} axis={xAxis} axisType="x" fill="white"/>
                                </g>

                            </g>
                        </svg>
                    </div>
                </div>
                <div className="col-md-4 legend">
                    {legend}
                </div>
            </div>

            
        );
    }

});
    

export default EquipmentReport;