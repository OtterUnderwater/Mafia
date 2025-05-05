import { EliminationReasonEnum, RoleEnum, StatusEnum } from '@/custom_types/enums.ts';

export interface Player {
  id: number;
  nickname: string;
  fouls: number;
  role: RoleEnum | null;
  status: StatusEnum;
  elimination_reason: EliminationReasonEnum | null;
  show_role: boolean;
}
