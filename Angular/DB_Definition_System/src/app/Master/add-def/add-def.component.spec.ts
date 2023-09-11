import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddDefComponent } from './add-def.component';

describe('AddDefComponent', () => {
  let component: AddDefComponent;
  let fixture: ComponentFixture<AddDefComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AddDefComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AddDefComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
