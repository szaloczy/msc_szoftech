import { Component, EventEmitter, Input, OnChanges, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-prompt-dialog',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './prompt-dialog.html',
  styleUrl: './prompt-dialog.css',
})
export class PromptDialog implements OnChanges {
  @Input() title = 'Enter information';
  @Input() message = 'Please enter the required information:';
  @Input() defaultValue = '';
  @Input() placeholder = '';
  @Input() confirmButtonText = 'OK';
  @Input() cancelButtonText = 'Cancel';
  @Input() showDialog = false;

  @Output() confirmed = new EventEmitter<string>();
  @Output() canceled = new EventEmitter<void>();
  @Output() showDialogChange = new EventEmitter<boolean>();

  inputValue = '';

  ngOnChanges() {
    if (this.showDialog) {
      this.inputValue = this.defaultValue;

      setTimeout(() => {
        const inputElement = document.querySelector('input[type="text"]') as HTMLInputElement;
        if (inputElement) {
          inputElement.focus();
          inputElement.select();
        }
      }, 0);
    }
  }

  onConfirm() {
    this.confirmed.emit(this.inputValue);
    this.closeDialog();
  }

  onCancel() {
    this.canceled.emit();
    this.closeDialog();
  }

  closeDialog() {
    this.showDialog = false;
    this.showDialogChange.emit(this.showDialog);
  }
}
