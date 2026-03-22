import { Component, OnInit } from '@angular/core';
import {environment} from '../environments/environments';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  standalone: false,
  styleUrl: './app.component.scss'
})
export class AppComponent implements OnInit {
  title = 'PowerStream';
constructor() {}

ngOnInit(): void {
  this.test();
}

test(){
  const data = environment.FastApiBaseUrl;
  console.log(data);

  
}


}
