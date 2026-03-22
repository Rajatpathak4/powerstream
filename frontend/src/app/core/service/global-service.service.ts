import { DatePipe } from '@angular/common';
import { Injectable } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import Swal, { SweetAlertIcon, SweetAlertOptions, SweetAlertResult } from 'sweetalert2'

declare const window: any;
@Injectable({
  providedIn: 'root'
})
export class GlobalServiceService {
  
constructor(public modalService: NgbModal, private readonly datePipe: DatePipe) {
  window.angularComponent = this;
}

getPreviousAndNextYears(): number[] {
  const currentYear = new Date().getFullYear();
  const years = Array.from({ length: 8 }, (_, index) => currentYear - 3 + index);    
  return years;
  }

getMonthList(){
 return [{ month: 'January', value: '1' },
    { month: 'February', value: '2' },
    { month: 'March', value: '3' },
    { month: 'April', value: '4' },
    { month: 'May', value: '5' },
    { month: 'June', value: '6' },
    { month: 'July', value: '7' },
    { month: 'August', value: '8' },
    { month: 'September', value: '9' },
    { month: 'October', value: '10' },
    { month: 'November', value: '11' },
    { month: 'December', value: '12' }];
 }

showToastr(message: string, type: SweetAlertIcon): void {
    const Toast: SweetAlertOptions = {
      toast: true,
      position: 'top-end',
      showConfirmButton: false,
      timer: 5000,
      timerProgressBar: true,
      icon: type,
      title: message
    };

    Swal.fire(Toast);
  }

triggerSweetAlert(alertOptions: SweetAlertOptions): Promise<SweetAlertResult<any>> {
  alertOptions.customClass = {
    popup: 'bg-dark',
    title: 'text-light',
    confirmButton: 'bg-success border-0',
    cancelButton: 'bg-danger ms-3',
    htmlContainer: 'text-light'
  }
  alertOptions.showCancelButton = alertOptions.showCancelButton === false ? false : true;
  alertOptions.focusConfirm = false;
  return Swal.fire(alertOptions);
  }
}
