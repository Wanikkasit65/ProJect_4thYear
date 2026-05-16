// Mock Geocoding for Chiang Mai locations
const MOCK_LOCATIONS = {
  '18.7883,98.9853': 'ประตูท่าแพ',
  '18.7970,98.9817': 'อ่างแก้ว มช.',
  '18.8036,98.9712': 'ดอยสุเทพ',
  '18.7769,98.9937': 'นิมมานเหมินทร์',
  default: 'เชียงใหม่'
};

function geocode(lat, lng) {
  const key = `${lat},${lng}`;
  return MOCK_LOCATIONS[key] || MOCK_LOCATIONS.default;
}

module.exports = { geocode };

