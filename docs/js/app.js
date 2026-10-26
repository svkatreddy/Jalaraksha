/**
 * JalaRaksha GitHub Pages Interactive Store (localStorage)
 * Allows reporting, tracking, surveys, and admin dashboard without requiring Python backend.
 */

const STORAGE_KEY_REPORTS = 'jalaraksha_reports_v1';
const STORAGE_KEY_SURVEYS = 'jalaraksha_surveys_v1';

// Seed demo data if storage is empty
function initStorage() {
  if (!localStorage.getItem(STORAGE_KEY_REPORTS)) {
    const defaultReports = [
      {
        reference_code: 'JR-DEMO0001A',
        category: 'Leaking tap/pipe',
        location_text: 'Engineering Block A, 1st floor water cooler',
        description: '[DEMO TEST RECORD] Minor drip observed from cooler inlet valve.',
        observed_on: '2026-10-24',
        status: 'Under Review',
        public_update: 'Report inspected by maintenance supervisor.',
        created_at: '2026-10-24 09:30:00'
      },
      {
        reference_code: 'JR-DEMO0002B',
        category: 'Overflowing tank',
        location_text: 'Hostel 3 Overhead Storage Tank',
        description: '[DEMO TEST RECORD] Tank overflow pipe running during morning pump cycle.',
        observed_on: '2026-10-21',
        status: 'Resolved',
        public_update: 'Float valve repaired and water level sensor recalibrated on Oct 24.',
        created_at: '2026-10-21 07:15:00'
      },
      {
        reference_code: 'JR-DEMO0003C',
        category: 'Damaged public water outlet',
        location_text: 'Main Campus Sports Ground Tap',
        description: '[DEMO TEST RECORD] Push-tap missing handle, continuous trickle.',
        observed_on: '2026-10-25',
        status: 'Submitted',
        public_update: 'Report received and queued for review.',
        created_at: '2026-10-25 14:00:00'
      }
    ];
    localStorage.setItem(STORAGE_KEY_REPORTS, JSON.stringify(defaultReports));
  }

  if (!localStorage.getItem(STORAGE_KEY_SURVEYS)) {
    const defaultSurveys = [
      {
        area_label: 'Campus Academic Zone',
        observed_wastage: 'Yes',
        categories: ['Leaking tap/pipe', 'Overflowing tank'],
        awareness_level: 'Moderate',
        rainwater_harvesting: 'Yes',
        suggestion: 'Place visual reminders near washbasins.',
        date: '2026-10-24'
      },
      {
        area_label: 'Hostel Complex',
        observed_wastage: 'Yes',
        categories: ['Overflowing tank'],
        awareness_level: 'High',
        rainwater_harvesting: 'Not sure',
        suggestion: 'Automated timer for overhead pump switches.',
        date: '2026-10-25'
      }
    ];
    localStorage.setItem(STORAGE_KEY_SURVEYS, JSON.stringify(defaultSurveys));
  }
}

initStorage();

function getReports() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY_REPORTS)) || [];
  } catch (e) {
    return [];
  }
}

function saveReport(report) {
  const reports = getReports();
  reports.unshift(report);
  localStorage.setItem(STORAGE_KEY_REPORTS, JSON.stringify(reports));
}

function getReportByCode(code) {
  if (!code) return null;
  const clean = code.trim().toUpperCase();
  const reports = getReports();
  return reports.find(r => r.reference_code.toUpperCase() === clean);
}

function generateReferenceCode() {
  const chars = '23456789ABCDEFGHJKLMNPQRSTUVWXYZ';
  let result = 'JR-';
  for (let i = 0; i < 10; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
}

function getSurveys() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY_SURVEYS)) || [];
  } catch (e) {
    return [];
  }
}

function saveSurvey(survey) {
  const surveys = getSurveys();
  surveys.unshift(survey);
  localStorage.setItem(STORAGE_KEY_SURVEYS, JSON.stringify(surveys));
}

// Mobile Navbar Toggle
document.addEventListener('DOMContentLoaded', () => {
  const toggleBtn = document.querySelector('.mobile-nav-toggle');
  const navMenu = document.querySelector('.nav-menu');
  if (toggleBtn && navMenu) {
    toggleBtn.addEventListener('click', () => {
      navMenu.classList.toggle('is-open');
    });
  }
});
