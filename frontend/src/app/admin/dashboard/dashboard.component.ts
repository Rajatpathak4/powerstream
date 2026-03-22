import { Component } from '@angular/core';
import * as Highcharts from "highcharts";

@Component({
  selector: 'app-dashboard',
  standalone: false,
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss'
})
export class DashboardComponent {
  chart: Highcharts.Chart
  
  constructor(){

  }

}
