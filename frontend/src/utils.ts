export function validateFiles(files: File[], existing: number, max=15, mb=15) {
 if (files.length+existing>max) return `Choose up to ${max} photos per collection.`;
 if(files.some(f=>!['image/jpeg','image/png','image/webp'].includes(f.type))) return 'Please use JPEG, PNG or WebP photos.';
 if(files.some(f=>f.size>mb*1024*1024)) return `Each photo must be under ${mb} MB.`;
 return '';
}
export function move(ids:string[],index:number,delta:number){const out=[...ids];const target=index+delta;if(target<0||target>=ids.length)return out;[out[index],out[target]]=[out[target],out[index]];return out;}
export function toggle(ids:string[],id:string){return ids.includes(id)?ids.filter(x=>x!==id):[...ids,id];}
export const validBrief=(s:string)=>s.trim().length>=5;
